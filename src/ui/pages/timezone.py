# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .global_state import global_state
from .page import Page
from .system_calls import set_system_timezone
from .timezone_provider import get_timezones
from .widgets import reset_model, ProgressRow


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/timezone.ui')
class TimezonePage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image = 'globe-symbolic'

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
            self.filter_list_model, lambda l: ProgressRow(l.name))

    def _filter(self, *args):
        self.search_text = self.search_entry.get_text().lower()
        self.custom_filter.set_filter_func(self._timezone_filter)

        if self.filter_list_model.get_n_items() > 0:
            self.stack.set_visible_child_name('list')
        else:
            self.stack.set_visible_child_name('none')

    def _timezone_filter(self, timezone):
        if self.search_text in timezone.lower_case_name:
            return True
        for location in timezone.locations:
            if self.search_text in location:
                return True
        return False

    ### callbacks ###

    @Gtk.Template.Callback('row_selected')
    def _row_selected(self, list_box, row):
        set_system_timezone(row.get_label())
        global_state.advance(self)

    ### public methods ###

    def load(self):
        if not self.list_loaded:
            self.list_loaded = True
            reset_model(self.list_model, get_timezones())
        return "load_next"
