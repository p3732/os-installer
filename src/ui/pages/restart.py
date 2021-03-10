# SPDX-License-Identifier: GPL-3.0-or-later

from .page import Page

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/restart.ui')
class RestartPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'system-reboot-symbolic'

    def __init__(self, global_state, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        self.global_state = global_state

    ### public methods ###

    def load(self):
        self.global_state.apply_restart()
