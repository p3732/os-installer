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

from gi.repository import Gtk, Handy

# The available pages in order
PAGES = [
    [  # section language
        LanguagePage
    ],
    [  # section pre-installation
        KeyboardLayoutPage,
        InternetPage,
        DiskPage,
        EncryptPage,
        ConfirmPage
    ],
    [  # section configuration
        UserPage,
        SoftwarePage,
        LocalePage
    ],
    [  # section installation
        InstallPage
    ],
    [  # section done
        DonePage
    ],
    [  # section restart
        RestartPage
    ]
]


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/main_window.ui')
class OsInstallerWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'OsInstallerWindow'

    content_box = Gtk.Template.Child()

    def __init__(self, global_state, quit_callback, **kwargs):
        super().__init__(**kwargs)

        self.quit_callback = quit_callback

        # setup stack
        main_stack = MainStack(PAGES, global_state)
        global_state.stack = main_stack
        self.content_box.add(main_stack)

    def show_about_dialog(self):
        builder = Gtk.Builder.new_from_resource(
            '/com/github/p3732/os-installer/about_dialog.ui'
        )
        about_dialog = builder.get_object('about_dialog')
        about_dialog.show_all()
        about_dialog.set_transient_for(self)
        about_dialog.set_modal(True)

    def show_failed_installation_dialog(self):
        popup = FailedInstallationPopup(self.quit_callback)
        popup.show_all()
        popup.set_transient_for(self)
        popup.set_modal(True)
