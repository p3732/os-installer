#from .install_provider import InstallProvider

import threading

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/install.ui')
class InstallPage(Gtk.Box):
    __gtype_name__ = 'InstallPage'

    terminal_box = Gtk.Template.Child()
    terminal_button = Gtk.Template.Child()
    stack = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        self.global_state = global_state
        self.vte_created = False

        self.installed_lock = threading.Lock()
        self.installed = False
        self.can_proceed_automatically = False

        # connect to (most likely ongoing) installation
        callback = self._on_installed
        # TODO
        #self.internet_provider = InstallationProvider(global_state, callback)

        # UI element states
        self.stack.set_visible_child_name('spinner')

        # signals
        self.terminal_button.connect('toggled', self._on_toggled_terminal_button)

    def _setup_vte(self):
        terminal = self.global_state.terminal
        self.terminal_box.add(terminal)
        self.terminal_box.show_all()

    ### callbacks ###

    def _on_toggled_terminal_button(self, toggle_button):
        if self.stack.get_visible_child_name() == 'spinner':
            if not self.vte_created:
                self._setup_vte()
                self.vte_created = True
            self.stack.set_visible_child_name('terminal')
        else:
            self.stack.set_visible_child_name('spinner')

    def _on_installed(self):
        with self.installed_lock:
            self.installed = True
        self.global_state.page_can_proceed_automatically(self.__gtype_name__)

    ### public methods ###

    def load(self):
        with self.installed_lock:
            if self.installed:
                return 'automatic'
        if self.global_state.demo_mode:
            return 'ok_to_proceed'

    def save(self):
        self.global_state.apply_installed()
