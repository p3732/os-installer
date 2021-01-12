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
        LocalePage,
        SoftwarePage
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

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        # setup stack
        main_stack = MainStack(PAGES, global_state)
        global_state.set_stack(main_stack)
        self.content_box.add(main_stack)
