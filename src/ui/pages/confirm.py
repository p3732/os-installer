# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/confirm.ui')
class ConfirmPage(Gtk.Box):
    __gtype_name__ = 'ConfirmPage'

    disk_label = Gtk.Template.Child()
    confirm_button = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        self.global_state = global_state

        # signals
        self.confirm_button.connect("clicked", self._on_clicked_confirm)

    ### callbacks ###

    def _on_clicked_confirm(self, button):
        self.global_state.apply_installation_confirmed()
        self.global_state.advance()

    ### public methods ###

    def load(self):
        # set label (always reload)
        name = self.global_state.get_config('disk_name')
        self.disk_label.set_label(name)

    def save(self):
        self.global_state.apply_installation_confirmed()
