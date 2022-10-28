# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .global_state import global_state
from .installation_scripting import installation_scripting
from .system_calls import open_internet_search
from .page import Page


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/failed.ui')
class FailedPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image = 'computer-fail-symbolic'

    page_title = Gtk.Template.Child()
    terminal_box = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

    ### callbacks ###

    @Gtk.Template.Callback('search_button_clicked')
    def _search_button_clicked(self, button):
        open_internet_search()

    ### public methods ###

    def load_once(self):
        self.terminal_box.append(installation_scripting.terminal)
        global_state.send_notification(self.page_title.get_label(),'')
