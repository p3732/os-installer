# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from threading import Lock

from gi.repository import Gtk, Adw

from .global_state import global_state

from .confirm import ConfirmPage
from .disk import DiskPage
from .done import DonePage
from .encrypt import EncryptPage
from .failed import FailedPage
from .format import FormatPage
from .install import InstallPage
from .internet import InternetPage
from .keyboard_layout import KeyboardLayoutPage
from .language import LanguagePage
from .locale import LocalePage
from .restart import RestartPage
from .software import SoftwarePage
from .summary import SummaryPage
from .timezone import TimezonePage
from .user import UserPage
from .welcome import WelcomePage
from .widgets import PageWrapper

from .confirm_quit_popup import ConfirmQuitPopup

from .language_provider import language_provider
from .system_calls import set_system_language


class Navigation:
    current: int = -1
    earliest: int = 0
    furthest: int = 0

    def set(self, state: int):
        self.current = state
        self.furthest = max(self.furthest, state)

    def is_not_earliest(self):
        return self.current > self.earliest

    def is_not_furthest(self):
        return self.current < self.furthest


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/main_window.ui')
class OsInstallerWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'OsInstallerWindow'

    image_stack = Gtk.Template.Child()
    main_stack = Gtk.Template.Child()

    next_revealer = Gtk.Template.Child()
    previous_revealer = Gtk.Template.Child()
    reload_revealer = Gtk.Template.Child()

    current_page = None
    # when changing pages by name return to this page on advancing
    original_page_name: str = ''
    navigation_lock = Lock()
    navigation = Navigation()
    pages = []

    def __init__(self, quit_callback, **kwargs):
        super().__init__(**kwargs)

        self.quit_callback = quit_callback

        # set advancing functions in global state
        global_state.advance = self.advance
        global_state.load_translated_pages = self.load_translated_pages
        global_state.navigate_to_page = self.navigate_to_page
        global_state.reload_title_image = self._reload_title_image
        global_state.installation_failed = self.show_failed_page

        # determine available pages
        self._determine_available_pages()

        if 'language' in self.available_pages:
            # only initialize language page, others depend on chosen language
            self._initialize_page('language')
        else:
            for page_name in self.available_pages.keys():
                self._initialize_page(page_name)

    def _determine_available_pages(self):
        # list page types tupled with condition on when to use
        pages = [
            # pre-installation section
            ('language', LanguagePage, self._offer_language_selection()),
            ('welcome', WelcomePage, global_state.get_config('welcome_page')['usage']),
            ('keyboard', KeyboardLayoutPage, True),
            ('internet', InternetPage, global_state.get_config(
                'internet_connection_required')),
            ('disk', DiskPage, True),
            ('encrypt', EncryptPage, global_state.get_config('offer_disk_encryption')),
            ('confirm', ConfirmPage, True),
            # configuration section
            ('user', UserPage, True),
            ('locale', LocalePage, True),
            ('format', FormatPage, True),
            ('timezone', TimezonePage, True),
            ('software', SoftwarePage, global_state.get_config('additional_software')),
            # summary
            ('summary', SummaryPage, True),
            # installation
            ('install', InstallPage, True),
            # post-installation
            ('done', DonePage, True),
            ('restart', RestartPage, True),
            # failed installation, keep at end
            ('failed', FailedPage, True)
        ]
        # filter out nonexistent pages
        self.available_pages = {page_name: page for page_name, page, condition in pages if condition}

    def _offer_language_selection(self):
            # only initialize language page, others depend on chosen language
        if fixed_language := global_state.get_config('fixed_language'):
            if fixed_info := language_provider.get_fixed_language(fixed_language):
                set_system_language(fixed_info)
                return False
        return True

    def _initialize_page(self, page_name):
        page_type = self.available_pages[page_name]
        page = PageWrapper(page_type())

        self.main_stack.add_named(page, page_name)
        self.pages.append(page_name)

    def _remove_pages(self, page_names):
        for page_name in page_names:
            child = self.main_stack.get_child_by_name(page_name)
            self.main_stack.remove(child)
            del child

    def _load_page(self, page_number: int):
        assert page_number >= 0, 'Tried to go to non-existent page (underflow)'
        assert page_number < len(self.pages), 'Tried to go to non-existent page (overflow)'

        # unload old page
        if self.current_page:
            self.current_page.unload()

        # load page
        page_name = self.pages[page_number]
        wrapper = self.main_stack.get_child_by_name(page_name)
        self.current_page = wrapper.get_page()

        match self.current_page.load():
            case "load_next":
                self._load_page(page_number + 1)
                return
            case "prevent_back_navigation":
                self.navigation.earliest = page_number

        self.main_stack.set_visible_child(wrapper)
        self.navigation.set(page_number)
        self._reload_title_image()
        self._update_navigation_buttons()
    def _load_page_by_name(self, page_name: str) -> None:
        self.current_page.unload()

        wrapper = self.main_stack.get_child_by_name(page_name)
        if wrapper == None:
            print(f'Page named {page_name} does not exist. Are you testing things and forget to comment it back in?')
            return
        self.current_page = wrapper.get_page()
        self.current_page.load()
        self.main_stack.set_visible_child(wrapper)

        self._reload_title_image()
        self.previous_revealer.set_reveal_child(True)
        self.next_revealer.set_reveal_child(False)
        self.reload_revealer.set_reveal_child(self.current_page.can_reload)

    def _load_original_page(self):
        self.current_page.unload()

        original_page = self.main_stack.get_child_by_name(self.original_page_name)
        self.current_page = original_page.get_page()
        self.current_page.load()
        self.main_stack.set_visible_child(original_page)
        self.original_page_name = None

        self._reload_title_image()
        self._update_navigation_buttons()

    def _reload_title_image(self):
        next_image_name = '1' if self.image_stack.get_visible_child_name() == '2' else '2'
        next_image = self.image_stack.get_child_by_name(next_image_name)
        image_source = self.current_page.image
        if isinstance(image_source, str):
            next_image.set_from_icon_name(image_source)
        elif isinstance(image_source, Path):
            next_image.set_from_file(str(image_source))
        else:
            print('Developer hint: invalid request to set title image')
            return # ignoring
        self.image_stack.set_visible_child_name(next_image_name)

    def _show_dialog(self, dialog):
        dialog.set_transient_for(self)
        dialog.set_modal(True)
        dialog.present()

    def _update_navigation_buttons(self):
        # backward
        show_backward = self.current_page.can_navigate_backward or self.navigation.is_not_earliest()
        self.previous_revealer.set_reveal_child(show_backward)

        # forward
        show_forward = self.current_page.can_navigate_forward or self.navigation.is_not_furthest()
        self.next_revealer.set_reveal_child(show_forward)

        # reload
        self.reload_revealer.set_reveal_child(self.current_page.can_reload)

    ### public methods ###

    def advance(self, page, allow_return: bool = True, cleanup: bool = False):
        if cleanup and allow_return:
            return print('Logic Error: Combining of return and cleanup not possible!')
        with self.navigation_lock:
            # confirm calling page is current page to prevent incorrect navigation
            if not page or page == self.current_page:
                if self.original_page_name:
                    if not allow_return:
                        return print('Logic Error: Returning unpreventable, page name mode')
                    self._load_original_page()
                else:
                    if not allow_return:
                        self.navigation.earliest = self.navigation.current + 1

                    self._load_page(self.navigation.current + 1)

                    if cleanup:
                        self._remove_pages(self.pages[:self.navigation.current - 1])

    def load_translated_pages(self):
        with self.navigation_lock:
            # delete pages that are not the language page
            self._remove_pages(self.pages[1:])
            self.pages = ['language']

            for page_name in self.available_pages.keys():
                if page_name != 'language':
                    self._initialize_page(page_name)

    def navigate_backward(self):
        with self.navigation_lock:
            if self.current_page.can_navigate_backward:
                self.current_page.navigate_backward()
            elif self.original_page_name:
                self._load_original_page()
            elif self.navigation.is_not_earliest():
                self._load_page(self.navigation.current - 1)

    def navigate_forward(self):
        with self.navigation_lock:
            if self.current_page.can_navigate_forward:
                self.current_page.navigate_forward()
            elif self.navigation.is_not_furthest():
                self._load_page(self.navigation.current + 1)

    def reload_page(self):
        with self.navigation_lock:
            if self.current_page.can_reload:
                self.current_page.load()

    def show_about_page(self):
        with self.navigation_lock:
            builder = Gtk.Builder.new_from_resource('/com/github/p3732/os-installer/ui/about_dialog.ui')
            popup = builder.get_object('about_window')
            if popup:
                self._show_dialog(popup)

    def show_confirm_quit_dialog(self):
        popup = ConfirmQuitPopup(self.quit_callback)
        self._show_dialog(popup)

    def show_failed_page(self):
        with self.navigation_lock:
            global_state.installation_running = False

            failed_page_position = len(self.available_pages)-1
            self.navigation.earliest = failed_page_position
            self._load_page(failed_page_position)

    def navigate_to_page(self, page_name):
        self.original_page_name = self.main_stack.get_visible_child_name()
        self._load_page_by_name(page_name)
