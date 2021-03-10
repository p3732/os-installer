# SPDX-License-Identifier: GPL-3.0-or-later

from .page import Page

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/confirm.ui')
class ConfirmPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'question-round-symbolic'

    disk_label = Gtk.Template.Child()
    confirm_button = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

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
