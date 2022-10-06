# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .global_state import global_state
from .locale_provider import get_current_formats, get_timezone
from .page import Page


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/locale.ui')
class LocalePage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image = 'globe-symbolic'

    formats_label = Gtk.Template.Child()
    timezone_label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

    ### callbacks ###

    @Gtk.Template.Callback('continue')
    def _continue(self, button):
        global_state.advance_without_return(self)

    @Gtk.Template.Callback('overview_row_activated')
    def _overview_row_activated(self, list_box, row):
        global_state.navigate_to_page(row.get_name())

    ### public methods ###

    def load(self):
        formats = global_state.get_config('formats_ui')
        if not formats:
            locale, name = get_current_formats()
            set_system_formats(locale, name)
            formats = global_state.set_config('formats_ui', name)
        self.formats_label.set_label(formats)

        timezone = global_state.get_config('timezone')
        if not timezone:
            timezone = get_timezone()
            global_state.set_config('timezone', timezone)
        self.timezone_label.set_label(timezone)
