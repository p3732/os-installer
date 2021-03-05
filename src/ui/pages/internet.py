# SPDX-License-Identifier: GPL-3.0-or-later

from .internet_provider import InternetProvider

import threading

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/internet.ui')
class InternetPage(Gtk.Box):
    __gtype_name__ = 'InternetPage'

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

        # signals
        self.settings_button.connect('clicked', self._on_clicked_settings_button)

    ### callbacks ###

    def _on_clicked_settings_button(self, button):
        self.global_state.open_wifi_settings()

    def _on_connected(self):
        notify_global_state = False

        with self.connected_lock:
            self.connected = True
            if self.can_proceed_automatically:
                notify_global_state = True
            self.global_state.apply_connected()

        # do not hold lock, could cause deadlock with simultaneous load()
        if notify_global_state:
            self.global_state.advance(self.__gtype_name__)

    ### public methods ###

    def load(self):
        if self.global_state.demo_mode:
            self.global_state.allow_forward_navigation()
        with self.connected_lock:
            if self.connected:
                if self.can_proceed_automatically:
                    # page was already loaded once, do not skip automatically
                    icon_name = 'network-wireless-symbolic'
                else:
                    icon_name = None
            else:
                icon_name = 'network-wireless-disabled-symbolic'
            self.can_proceed_automatically = True
            return icon_name
