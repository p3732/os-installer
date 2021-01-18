from .widgets import empty_list, BackRow, ProgressRow

from gi.repository import Gtk, GWeather


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/timezone_chooser.ui')
class TimezoneChooser(Gtk.Stack):
    __gtype_name__ = 'TimezoneChooser'

    continents_list = Gtk.Template.Child()
    countries_list = Gtk.Template.Child()
    subzones_list = Gtk.Template.Child()

    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)

        self.callback = callback
        self.continents_list_loaded = False

        # signals
        self.continents_list.connect('row-activated', self._on_continent_row_activated)
        self.countries_list.connect('row-activated', self._on_country_row_activated)
        self.subzones_list.connect('row-activated', self._on_subzone_row_activated)

    def _add_location_children_to_list(self, location, list_box):
        for sub_location in location.get_children():
            row = ProgressRow(sub_location.get_name(), sub_location)
            list_box.add(row)

    def _load_continents_list(self):
        # fill if needed
        if not self.continents_list_loaded:
            world = GWeather.Location.get_world()
            self._add_location_children_to_list(world, self.continents_list)
            self.continents_list_loaded = True

        # show
        self.set_visible_child_name('continents')

    def _load_countries_list(self, continent):
        # empty
        empty_list(self.countries_list)

        # back row
        row = BackRow(continent.get_name())
        self.countries_list.add(row)

        # add countries
        self._add_location_children_to_list(continent, self.countries_list)

        # show
        self.set_visible_child_name('countries')

    def _load_subzones_list(self, country):
        # empty
        empty_list(self.subzones_list)

        # back row
        row = BackRow(country.get_name())
        self.subzones_list.add(row)

        # fill
        for subzone in country.get_children():
            if not subzone.get_timezone() == None:
                row = ProgressRow(subzone.get_name(), subzone)
                self.subzones_list.add(row)

        # show
        self.set_visible_child_name('subzones')

    ### callbacks ###

    def _on_continent_row_activated(self, list_box, row):
        continent = row.get_info()
        self._load_countries_list(continent)

    def _on_country_row_activated(self, list_box, row):
        if row.get_name() == 'back_row':
            self.set_visible_child_name('continents')
        else:
            # check if country has timezone
            country = row.get_info()
            timezone = country.get_timezone_str()
            if not timezone:
                self._load_subzones_list(country)
            else:
                self.callback(timezone)

    def _on_subzone_row_activated(self, list_box, row):
        if row.get_name() == 'back_row':
            self.set_visible_child_name('countries')
        else:
            subzone = row.get_info()
            timezone = subzone.get_timezone_str()

            if not subzone:
                print('Subzone', subzone, 'does not have any timezone attached to it! Falling back to UTC.')
                # TODO timezone = utc
            self.callback(timezone)

    ### public methods ###

    def load(self):
        self._load_continents_list()
