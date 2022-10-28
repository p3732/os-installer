# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, Gtk

from .format_provider import get_formats
from .global_state import global_state
from .page import Page
from .system_calls import set_system_formats
from .widgets import reset_model, ProgressRow


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/format.ui')
class FormatPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image = 'map-symbolic'

    search_entry = Gtk.Template.Child()
    custom_filter = Gtk.Template.Child()
    filter_list_model = Gtk.Template.Child()

    stack = Gtk.Template.Child()
    list = Gtk.Template.Child()
    list_loaded = False
    list_model = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        self.search_entry.connect("search-changed", self._filter)

        self.list.bind_model(
            self.filter_list_model, lambda f: ProgressRow(f.name))

    def _filter(self, *args):
        self.search_text = self.search_entry.get_text().lower()
        self.custom_filter.set_filter_func(self.format_filter)

        if self.filter_list_model.get_n_items() > 0:
            self.stack.set_visible_child_name('list')
        else:
            self.stack.set_visible_child_name('none')

    def format_filter(self, format):
        return self.search_text in format.lower_case_name or format.locale.startswith(self.search_text)

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
        return "load_next"
