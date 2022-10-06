# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, Gtk

from .global_state import global_state
from .locale_provider import get_formats
from .page import Page
from .system_calls import set_system_formats
from .widgets import reset_model, ProgressRow


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/format.ui')
class FormatPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image = 'map-symbolic'

    list = Gtk.Template.Child()
    list_loaded = False
    list_model = Gio.ListStore()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        self.list.bind_model(
            self.list_model, lambda f: ProgressRow(f.name, f.locale))

    ### callbacks ###

    @Gtk.Template.Callback('formats_selected')
    def _formats_selected(self, list_box, row):
        set_system_formats(row.info, row.get_label())
        global_state.advance(self)
    ### public methods ###

    def load(self):
        if not self.list_loaded:
            self.list_loaded = True
            formats = get_formats()
            reset_model(self.list_model, formats)
        return True
