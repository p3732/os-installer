# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, Gtk, GWeather

from .global_state import global_state
from .installation_scripting import installation_scripting, Step
from .locale_provider import get_current_formats, get_formats, get_timezone
from .page import Page
from .system_calls import set_system_formats, set_system_timezone
from .widgets import reset_model, ProgressRow


def get_location_children(location):
    # this code is un-pythonesque because libgweather decided to simplify their API too much
    children = [location.next_child(None)]
    while child := location.next_child(children[-1]):
        children.append(child)
    return children

def create_location_row(location):
    return ProgressRow(location.get_name(), location)


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/locale.ui')
class LocalePage(Gtk.Stack, Page):
    __gtype_name__ = __qualname__
    image = 'globe-symbolic'

    # overview
    formats_label = Gtk.Template.Child()
    timezone_label = Gtk.Template.Child()

    # formats
    formats_list = Gtk.Template.Child()
    formats_list_loaded = False
    formats_list_model = Gio.ListStore()

    # locale
    timezone_stack = Gtk.Template.Child()
    continents_list = Gtk.Template.Child()
    continents_list_loaded = False
    countries_list = Gtk.Template.Child()
    subzones_list = Gtk.Template.Child()

    continents_list_model = Gio.ListStore()
    countries_list_model = Gio.ListStore()
    subzones_list_model = Gio.ListStore()


    def __init__(self, **kwargs):
        Gtk.Stack.__init__(self, **kwargs)

        self.formats_list.bind_model(
            self.formats_list_model, lambda f: ProgressRow(f.name, f.locale))
        self.countries_list.bind_model(self.countries_list_model, create_location_row)
        self.continents_list.bind_model(self.continents_list_model, create_location_row)
        self.subzones_list.bind_model(self.subzones_list_model, create_location_row)

    def _load_continents_list(self):
        if not self.continents_list_loaded:
            self.continents_list_loaded = True

            continents = []
            for continent in get_location_children(GWeather.Location.get_world()):
                if not continent.get_timezone():  # skip dummy locations
                    continents.append(continent)            
            reset_model(self.continents_list_model, continents)

        self.set_visible_child_name('timezone')
        self.timezone_stack.set_visible_child_name('continents')

    def _load_countries_list(self, continent):
        countries = get_location_children(continent)
        reset_model(self.countries_list_model, countries)

        self.timezone_stack.set_visible_child_name('countries')

    def _load_formats_list(self):
        if not self.formats_list_loaded:
            self.formats_list_loaded = True
            formats = get_formats()
            reset_model(self.formats_list_model, formats)

        self.set_visible_child_name('formats')

    def _load_subzones_list(self, country):
        subzones = []
        for subzone in get_location_children(country):
            if subzone.get_timezone():
                subzones.append(subzone)
        reset_model(self.subzones_list_model, subzones)

        self.timezone_stack.set_visible_child_name('subzones')

    def _set_formats(self, formats_locale, name):
        set_system_formats(formats_locale, name)
        self.formats_label.set_label(name)

    def _set_timezone(self, timezone):
        set_system_timezone(timezone)

        self.timezone_label.set_label(timezone)
        self._show_overview()

    def _show_overview(self):
        self.set_visible_child_name('overview')
        self.can_navigate_backward = False

    ### callbacks ###

    @Gtk.Template.Callback('confirmed')
    def _confirmed(self, button):
        installation_scripting.set_ok_to_start_step(Step.configure)
        global_state.advance_without_return(self)

    @Gtk.Template.Callback('formats_selected')
    def _formats_selected(self, list_box, row):
        self._set_formats(row.info, row.get_label())
        self._show_overview()

    @Gtk.Template.Callback('overview_row_activated')
    def _overview_row_activated(self, list_box, row):
        match row.get_name():
            case 'timezone':
                self._load_continents_list()
            case 'formats':
                self._load_formats_list()
        self.can_navigate_backward = True

    @Gtk.Template.Callback('timezone_selected')
    def _timezone_selected(self, list_box, row):
        location = row.info
        if (timezone :=  location.get_timezone_str()):
            self._set_timezone(timezone)
        elif list_box == self.subzones_list:
            print('Subzone', location.get_name(), 'does not have any timezone attached to it! Falling back to UTC.')
            self._set_timezone('UTC')
        elif list_box == self.continents_list:
            self._load_countries_list(location)
        elif list_box == self.countries_list:
            self._load_subzones_list(location)

    ### public methods ###

    def load_once(self):
        locale, name = get_current_formats()
        self._set_formats(locale, name)

        timezone = get_timezone()
        self.timezone_label.set_label(timezone)
        global_state.set_config('timezone', timezone)

    def navigate_backward(self):
        match (self.get_visible_child_name(), self.timezone_stack.get_visible_child_name()):
            case ("timezone", 'countries'):
                self.timezone_stack.set_visible_child_name('continents')
            case ("timezone", 'subzones'):
                self.timezone_stack.set_visible_child_name('countries')
            case _,_:
                self._show_overview()
