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
from .install import InstallPage
from .internet import InternetPage
from .keyboard_layout import KeyboardLayoutPage
from .language import LanguagePage
from .locale import LocalePage
from .restart import RestartPage
from .software import SoftwarePage
from .user import UserPage
from .welcome import WelcomePage
from .widgets import PageWrapper

from .confirm_quit_popup import ConfirmQuitPopup

from .language_provider import language_provider
from .system_calls import set_system_language


class NavigationState:
    current: int = -1
    earliest: int = 0
    furthest: int = 0

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
    navigation_lock = Lock()
    navigation_state = NavigationState()
    pages = []

    def __init__(self, quit_callback, **kwargs):
        super().__init__(**kwargs)

        self.quit_callback = quit_callback

        # set advancing functions in global state
        global_state.advance = self.advance
        global_state.advance_without_return = self.advance_without_return
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
            ('software', SoftwarePage, global_state.get_config('additional_software')),
            ('locale', LocalePage, True),
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

    def _initialize_pages_translated(self):
        # delete pages that are not the language page
        self._remove_pages(self.pages[1:])
        self.pages = ['language']

        for page_name in self.available_pages.keys():
            if page_name != 'language':
                self._initialize_page(page_name)

    def _remove_pages(self, page_names):
        for page_name in page_names:
            child = self.main_stack.get_child_by_name(page_name)
            self.main_stack.remove(child)

    def _load_page(self, page_number):
        # special case language page
        if type(self.current_page) == LanguagePage:
            self._initialize_pages_translated()

        assert page_number >= 0, 'Tried to go to non-existent page (underflow)'
        assert page_number < len(self.pages), 'Tried to go to non-existent page (overflow)'

        # unload previous page
        if self.current_page:
            self.current_page.unload()

        self.navigation_state.current = page_number
        self.navigation_state.furthest = max(self.navigation_state.furthest, page_number)

        # load page
        current_page_name = self.pages[self.navigation_state.current]
        wrapper = self.main_stack.get_child_by_name(current_page_name)
        self.current_page = wrapper.get_page()
        if not self.current_page.load():
            self.main_stack.set_visible_child(wrapper)
            self._reload_title_image()
            self._update_navigation_buttons()
        else:  # load next if load() returned True
            self._load_page(self.navigation_state.current + 1)

    def _reload_title_image(self):
        name = '1' if self.image_stack.get_visible_child_name() == '2' else '2'
        new_image = self.image_stack.get_child_by_name(name)
        image_source = self.current_page.image
        if isinstance(image_source, str):
            new_image.set_from_icon_name(image_source)
        elif isinstance(image_source, Path):
            new_image.set_from_file(str(image_source))
        else:
            print('Developer hint: invalid request to set title image')
            return # ignoring
        self.image_stack.set_visible_child_name(name)

    def _show_dialog(self, dialog):
        dialog.set_transient_for(self)
        dialog.set_modal(True)
        dialog.present()

    def _update_navigation_buttons(self):
        # backward
        show_backward = self.current_page.can_navigate_backward or self.navigation_state.is_not_earliest()
        self.previous_revealer.set_reveal_child(show_backward)

        # forward
        show_forward = self.current_page.can_navigate_forward or self.navigation_state.is_not_furthest()
        self.next_revealer.set_reveal_child(show_forward)

        # reload
        self.reload_revealer.set_reveal_child(self.current_page.can_reload)

    ### public methods ###

    def advance(self, page):
        with self.navigation_lock:
            # to prevent incorrect navigation, confirm that calling page is current page
            if not page or page.id() == self.current_page.id():
                self._load_page(self.navigation_state.current + 1)

    def advance_without_return(self, page):
        with self.navigation_lock:
            if not page or page.id() == self.current_page.id():
                previous_pages = self.pages[self.navigation_state.earliest:self.navigation_state.current]
                self.navigation_state.earliest = self.navigation_state.current + 1

                self._load_page(self.navigation_state.current + 1)

                for page in previous_pages:
                    del page

    def navigate_backward(self):
        with self.navigation_lock:
            if self.current_page.can_navigate_backward:
                self.current_page.navigate_backward()
            elif self.navigation_state.is_not_earliest():
                self._load_page(self.navigation_state.current - 1)

    def navigate_forward(self):
        with self.navigation_lock:
            if self.current_page.can_navigate_forward:
                self.current_page.navigate_forward()
            elif self.navigation_state.is_not_furthest():
                self._load_page(self.navigation_state.current + 1)

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
            self.navigation_state.earliest = failed_page_position
            self._load_page(failed_page_position)
