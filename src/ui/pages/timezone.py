# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, Gtk, GWeather

from .global_state import global_state
from .page import Page
from .system_calls import set_system_timezone
from .widgets import reset_model, ProgressRow


def get_location_children(location):
    # this code is un-pythonesque because libgweather decided to simplify their API too much
    children = [location.next_child(None)]
    while child := location.next_child(children[-1]):
        children.append(child)
    return children


def create_location_row(location):
    return ProgressRow(location.get_name(), location)


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/timezone.ui')
class TimezonePage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image = 'globe-symbolic'

    list_stack = Gtk.Template.Child()
    continents = Gtk.Template.Child()
    continents_loaded = False
    countries = Gtk.Template.Child()
    subzones = Gtk.Template.Child()

    continents_model = Gio.ListStore()
    countries_model = Gio.ListStore()
    subzones_model = Gio.ListStore()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        self.countries.bind_model(self.countries_model, create_location_row)
        self.continents.bind_model(self.continents_model, create_location_row)
        self.subzones.bind_model(self.subzones_model, create_location_row)

    def _load_countries(self, continent):
        countries = get_location_children(continent)
        reset_model(self.countries_model, countries)

        self.list_stack.set_visible_child_name('countries')

    def _load_subzones(self, country):
        subzones = []
        for subzone in get_location_children(country):
            if subzone.get_timezone():
                subzones.append(subzone)
        reset_model(self.subzones_model, subzones)

        self.list_stack.set_visible_child_name('subzones')

    def _set_timezone(self, timezone):
        self.can_navigate_backward = False
        set_system_timezone(timezone)
        global_state.advance(self)

    ### callbacks ###

    @Gtk.Template.Callback('timezone_selected')
    def _timezone_selected(self, list_box, row):
        location = row.info
        if (timezone := location.get_timezone_str()):
            self._set_timezone(timezone)
        elif list_box == self.subzones:
            print(f'Subzone {location.get_name()} does not have any'
                  ' timezone attached to it! Falling back to UTC.')
            self._set_timezone('UTC')
        elif list_box == self.continents:
            self._load_countries(location)
            self.can_navigate_backward = True
        elif list_box == self.countries:
            self._load_subzones(location)
            self.can_navigate_backward = True

    ### public methods ###

    def load(self):
        if not self.continents_loaded:
            self.continents_loaded = True

            continents = []
            for continent in get_location_children(GWeather.Location.get_world()):
                if not continent.get_timezone():  # skip dummy locations
                    continents.append(continent)
            reset_model(self.continents_model, continents)

        self.list_stack.set_visible_child_name('continents')
        return True

    def navigate_backward(self):
        match self.list_stack.get_visible_child_name():
            case 'countries':
                self.list_stack.set_visible_child_name('continents')
                self.can_navigate_backward = False
            case 'subzones':
                self.list_stack.set_visible_child_name('countries')
