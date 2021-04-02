# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .installation_scripting import installation_scripting
from .page import Page


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/failed.ui')
class FailedPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'computer-fail-symbolic'

    terminal_box = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

    ### public methods ###

    def load_once(self):
        self.terminal_box.add(installation_scripting.terminal)
        self.terminal_box.show_all()
