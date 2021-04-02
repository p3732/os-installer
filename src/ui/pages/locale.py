# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import GLib, Gtk, GWeather

from .global_state import global_state
from .installation_scripting import installation_scripting
from .locale_provider import get_current_formats, get_formats, get_timezone
from .page import Page
from .system_calls import set_system_formats, set_system_timezone
from .widgets import ProgressRow, empty_list


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/locale.ui')
class LocalePage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'globe-symbolic'

    text_stack = Gtk.Template.Child()
    list_stack = Gtk.Template.Child()

    # overview
    overview_list = Gtk.Template.Child()
    formats_label = Gtk.Template.Child()
    timezone_label = Gtk.Template.Child()
    confirm_button = Gtk.Template.Child()

    # formats
    formats_list = Gtk.Template.Child()
    formats_list_loaded = False

    # locale
    continents_list = Gtk.Template.Child()
    countries_list = Gtk.Template.Child()
    subzones_list = Gtk.Template.Child()
    continents_list_loaded = False

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        # signals
        self.overview_list.connect('row-activated', self._on_overview_row_activated)
        self.confirm_button.connect('clicked', self._on_clicked_confirm_button)
        self.formats_list.connect('row-activated', self._on_formats_row_activated)
        for timezone_list in [self.continents_list, self.countries_list, self.subzones_list]:
            timezone_list.connect('row-activated', self._on_timezone_row_activated)

    def _load_continents_list(self):
        if not self.continents_list_loaded:
            self.continents_list_loaded = True
            for continent in GWeather.Location.get_world().get_children():
                if not continent.get_timezone():  # skip dummy locations
                    self.continents_list.add(ProgressRow(continent.get_name(), continent))

        self.list_stack.set_visible_child_name('timezone_continents')
        self.text_stack.set_visible_child_name('timezone')

    def _load_countries_list(self, continent):
        empty_list(self.countries_list)

        for country in continent.get_children():
            self.countries_list.add(ProgressRow(country.get_name(), country))

        self.list_stack.set_visible_child_name('timezone_countries')

    def _load_formats_list(self):
        if not self.formats_list_loaded:
            self.formats_list_loaded = True
            for name, locale in get_formats():
                self.formats_list.add(ProgressRow(name, locale))

        self.text_stack.set_visible_child_name('formats')
        self.list_stack.set_visible_child_name('formats')

    def _load_subzones_list(self, country):
        empty_list(self.subzones_list)

        for subzone in country.get_children():
            if subzone.get_timezone():
                self.subzones_list.add(ProgressRow(subzone.get_name(), subzone))

        self.list_stack.set_visible_child_name('timezone_subzones')

    def _set_timezone(self, timezone):
        set_system_timezone(timezone)

        self.timezone_label.set_label(timezone)
        self._show_overview()

    def _show_overview(self):
        self.text_stack.set_visible_child_name('overview')
        self.list_stack.set_visible_child_name('overview')
        self.can_navigate_backward = False

    ### callbacks ###

    def _on_clicked_confirm_button(self, button):
        installation_scripting.start_next_step()
        global_state.advance_without_return(self.__gtype_name__)

    def _on_formats_row_activated(self, list_box, row):
        set_system_formats(row.info)

        self.formats_label.set_label(row.get_label())
        self._show_overview()

    def _on_overview_row_activated(self, list_box, row):
        if row.get_name() == 'timezone':
            self._load_continents_list()
        elif row.get_name() == 'formats':
            self._load_formats_list()
        self.can_navigate_backward = True

    def _on_timezone_row_activated(self, list_box, row):
        list_box.select_row(row)
        location = row.info
        timezone = location.get_timezone_str()
        if timezone:
            self._set_timezone(timezone)
        elif list_box == self.subzones_list:
            print('Subzone', subzone, 'does not have any timezone attached to it! Falling back to UTC.')
            self._set_timezone('UTC')
        elif list_box == self.continents_list:
            self._load_countries_list(location)
        elif list_box == self.countries_list:
            self._load_subzones_list(location)

    ### public methods ###

    def load_once(self):
        name, locale = get_current_formats()
        self.formats_label.set_label(name)
        global_state.set_config('formats', locale)

        timezone = get_timezone()
        self.timezone_label.set_label(timezone)
        global_state.set_config('timezone', timezone)

    def navigate_backward(self):
        current_list = self.list_stack.get_visible_child()
        if current_list == self.formats_list or current_list == self.continents_list:
            self._show_overview()
        elif current_list == self.countries_list:
            self.list_stack.set_visible_child_name('timezone_continents')
        elif current_list == self.subzones_list:
            self.list_stack.set_visible_child_name('timezone_countries')
