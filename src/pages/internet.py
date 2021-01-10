from .internet_provider import InternetProvider

import threading

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/internet.ui')
class InternetPage(Gtk.Box):
    __gtype_name__ = 'InternetPage'

    stack = Gtk.Template.Child()
    settings_button = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        self.global_state = global_state

        self.connected_lock = threading.Lock()
        self.connected = False
        self.can_proceed_automatically = False

        # start checking of connection
        callback = self._on_connected
        self.internet_provider = InternetProvider(global_state, callback)

        # UI element states
        self.stack.set_visible_child_name('disabled')

        # signals
        self.settings_button.connect('clicked', self._on_clicked_settings_button)

    ### callbacks ###

    def _on_clicked_settings_button(self, button):
        self.global_state.open_settings('wifi')

    def _on_connected(self):
        notify_global_state = False

        with self.connected_lock:
            self.connected = True
            self.stack.set_visible_child_name('enabled')
            if self.can_proceed_automatically:
                notify_global_state = True

        # do not hold lock, could cause deadlock with simultaneous load()
        if notify_global_state:
            self.global_state.page_can_proceed_automatically(self.__gtype_name__)
        self.global_state.apply_connected()

    ### public methods ###

    def load(self):
        with self.connected_lock:
            if self.connected:
                if self.can_proceed_automatically:
                    # page was already loaded once, do not skip automatically
                    return
                else:
                    self.can_proceed_automatically = True
                    return 'automatic'
            else:
                return 'waiting'
