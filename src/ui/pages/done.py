# SPDX-License-Identifier: GPL-3.0-or-later

from .page import Page

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/done.ui')
class DonePage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'checkbox-checked-symbolic'

    restart_button = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        self.global_state = global_state

        # signals
        self.restart_button.connect('clicked', self._on_restart_button_clicked)

    ### callbacks ###

    def _on_restart_button_clicked(self, button):
        self.global_state.advance_without_return()
