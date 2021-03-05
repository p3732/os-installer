# SPDX-License-Identifier: GPL-3.0-or-later

from .stack_manager import StackManager

from .confirm import ConfirmPage
from .disk import DiskPage
from .done import DonePage
from .encrypt import EncryptPage
from .install import InstallPage
from .internet import InternetPage
from .keyboard_layout import KeyboardLayoutPage
from .language import LanguagePage
from .locale import LocalePage
from .restart import RestartPage
from .software import SoftwarePage
from .user import UserPage

from .confirm_quit_popup import ConfirmQuitPopup
from .failed_installation_popup import FailedInstallationPopup

from gi.repository import Gtk, Handy


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/main_window.ui')
class OsInstallerWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'OsInstallerWindow'

    main_stack = Gtk.Template.Child()
    image_stack = Gtk.Template.Child()
    previous_stack = Gtk.Template.Child()
    next_stack = Gtk.Template.Child()

    def __init__(self, global_state, quit_callback, **kwargs):
        super().__init__(**kwargs)

        self.quit_callback = quit_callback

        available_pages = self._determine_available_pages(global_state.get_config)

        # stack manager
        stacks = (self.main_stack, self.image_stack, self.previous_stack, self.next_stack)
        stack_manager = StackManager(stacks, available_pages, global_state)
        global_state.stack = stack_manager

    def _determine_available_pages(self, get_config):
        # pre-installation section
        pre_installation_section = [KeyboardLayoutPage]
        if get_config('internet_connection_required'):
            pre_installation_section.append(InternetPage)
        pre_installation_section.append(DiskPage)
        if get_config('offer_disk_encryption'):
            pre_installation_section.append(EncryptPage)
        pre_installation_section.append(ConfirmPage)

        # configuration section
        configuration_section = [UserPage]
        additional_software = get_config('additional_software')
        if additional_software and len(additional_software) > 0:
            configuration_section.append(SoftwarePage)
        configuration_section.append(LocalePage)

        return [
            [LanguagePage],
            pre_installation_section,
            configuration_section,
            [InstallPage],
            [DonePage],
            [RestartPage]
        ]

    def _set_image(self, icon_name):
        current = self.image_stack.get_visible_child_name()
        other = '1' if current == '2' else '2'
        image = self.image_stack.get_child_by_name(other)
        image.set_from_icon_name(icon_name, 0)
        self.image_stack.set_visible_child_name(other)

    ### public methods ###

    def show_about_dialog(self):
        builder = Gtk.Builder.new_from_resource(
            '/com/github/p3732/os-installer/about_dialog.ui'
        )
        about_dialog = builder.get_object('about_dialog')
        about_dialog.show_all()
        about_dialog.set_transient_for(self)
        about_dialog.set_modal(True)

    def show_confirm_quit_dialog(self):
        popup = ConfirmQuitPopup(self.quit_callback)
        popup.show_all()
        popup.set_transient_for(self)
        popup.set_modal(True)

    def show_failed_installation_dialog(self, error_text):
        popup = FailedInstallationPopup(self.quit_callback, error_text)
        popup.show_all()
        popup.set_transient_for(self)
        popup.set_modal(True)
