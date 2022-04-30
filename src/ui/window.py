# SPDX-License-Identifier: GPL-3.0-or-later

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
from .widgets import PageWrapper

from .confirm_quit_popup import ConfirmQuitPopup


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
        global_state.installation_failed = self.show_failed_page

        # determine available pages
        self._determine_available_pages()

        # initialize language page
        self._initialize_page(self.available_pages[0])

    def _determine_available_pages(self):
        offer_internet_connection = global_state.get_config('internet_connection_required')
        offer_disk_encryption = global_state.get_config('offer_disk_encryption')
        offer_additional_software = len(global_state.get_config('additional_software')) > 0

        self.available_pages = [
            # pre-installation section
            LanguagePage,
            KeyboardLayoutPage,
            InternetPage if offer_internet_connection else None,
            DiskPage,
            EncryptPage if offer_disk_encryption else None,
            ConfirmPage,
            # configuration section
            UserPage,
            SoftwarePage if offer_additional_software else None,
            LocalePage,
            # installation
            InstallPage,
            # post-installation
            DonePage,
            RestartPage,
            # failed installation, keep at end
            FailedPage
        ]

    def _initialize_page(self, page_to_initialize):
        page = page_to_initialize()
        wrapper = PageWrapper(page)

        page_id = page.id()
        self.main_stack.add_named(wrapper, page_id)
        self.pages.append(page_id)

    def _initialize_pages_translated(self):
        # delete pages that are not the language page
        self._remove_pages(self.pages[1:])
        self.pages = [self.current_page.id()]

        for unintialized_page in self.available_pages[1:]:
            self._initialize_page(unintialized_page)

    def _remove_pages(self, page_ids):
        for page_id in page_ids:
            child = self.main_stack.get_child_by_name(page_id)
            self.main_stack.remove(child)

    def _load_page(self, page_number):
        # special case language page
        if self.navigation_state.current == 0:
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

            # set icon
            name = '1' if self.image_stack.get_visible_child_name() == '2' else '2'
            new_image = self.image_stack.get_child_by_name(name)
            new_image.set_from_icon_name(self.current_page.image_name)
            self.image_stack.set_visible_child_name(name)

            self._update_navigation_buttons()
        else:  # load next if load() returned True
            self._load_page(self.navigation_state.current + 1)

    def _show_dialog(self, dialog):
        dialog.set_transient_for(self)
        dialog.set_modal(True)

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
            self.current_page.load()

    def show_confirm_quit_dialog(self):
        popup = ConfirmQuitPopup(self.quit_callback)
        self._show_dialog(popup)

    def show_failed_page(self):
        with self.navigation_lock:
            global_state.installation_running = False

            failed_page_position = len(self.available_pages)-1
            self.navigation_state.earliest = failed_page_position
            self._load_page(failed_page_position)
