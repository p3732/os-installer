from .main_stack import MainStack

from .confirm import ConfirmPage
from .disk import DiskPage
from .encrypt import EncryptPage
from .internet import InternetPage
from .keyboard_layout import KeyboardLayoutPage
from .language import LanguagePage
#from .locale import LocalePage
from .user import UserPage

from gi.repository import Gtk, Handy


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/main_window.ui')
class OsInstallerWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'OsInstallerWindow'

    content_box = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        # Set default window icon for window managers
        self.set_default_icon_name('com.github.p3732.OS-Installer')

        # The available pages in order
        pages = [
            [  # section pre-installation
                LanguagePage(global_state),
                KeyboardLayoutPage(global_state),
                InternetPage(global_state),
                DiskPage(global_state),
                EncryptPage(global_state),
                ConfirmPage(global_state)
            ],
            [  # section configuration
                UserPage(global_state),
                # LocalePage(global_state),
            ]
        ]

        # setup stack
        main_stack = MainStack(pages)
        global_state.set_stack(main_stack)
        self.content_box.add(main_stack)
