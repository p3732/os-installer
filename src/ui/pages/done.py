# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/done.ui')
class DonePage(Gtk.Box):
    __gtype_name__ = 'DonePage'

    restart_button = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        self.global_state = global_state

        # signals
        self.restart_button.connect('clicked', self._on_restart_button_clicked)

    ### callbacks ###

    def _on_restart_button_clicked(self, button):
        self.global_state.advance()

    ### public methods ###

    def load(self):
        return 'checkbox-checked-symbolic'
