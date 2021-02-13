# SPDX-License-Identifier: GPL-3.0-or-later

from .main_stack import MainStack

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

    content_box = Gtk.Template.Child()

    def __init__(self, global_state, quit_callback, **kwargs):
        super().__init__(**kwargs)

        self.quit_callback = quit_callback

        available_pages = self._determine_available_pages(global_state.get_config)

        # setup stack
        main_stack = MainStack(available_pages, global_state)
        global_state.stack = main_stack
        self.content_box.add(main_stack)

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
