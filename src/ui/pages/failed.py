# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .installation_scripting import installation_scripting
from .system_calls import open_internet_search
from .page import Page


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/failed.ui')
class FailedPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'computer-fail-symbolic'

    terminal_box = Gtk.Template.Child()
    search_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)
        self.search_button.connect('clicked', self._on_search_button_clicked)

    ### callbacks ###

    def _on_search_button_clicked(self, button):
        open_internet_search()

    ### public methods ###

    def load_once(self):
        self.terminal_box.append(installation_scripting.terminal)
        #self.terminal_box.show_all()
