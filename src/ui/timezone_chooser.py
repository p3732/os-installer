from .widgets import empty_list, BackRow, ProgressRow

from gi.repository import Gtk, GWeather


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/timezone_chooser.ui')
class TimezoneChooser(Gtk.Box):
    __gtype_name__ = 'TimezoneChooser'

    stack = Gtk.Template.Child()

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

    def _load_continents_list(self):
        # fill if needed
        if not self.continents_list_loaded:
            world = GWeather.Location.get_world()
            for continent in world.get_children():
                # skip dummy locations with timezone
                if not continent.get_timezone():
                    row = ProgressRow(continent.get_name(), continent)
                    self.continents_list.add(row)

            self.continents_list_loaded = True

        # show
        self.stack.set_visible_child_name('continents')

    def _load_countries_list(self, continent):
        # empty
        empty_list(self.countries_list)

        # back row
        row = BackRow(continent.get_name())
        self.countries_list.add(row)

        # add countries
        for country in continent.get_children():
            row = ProgressRow(country.get_name(), country)
            self.countries_list.add(row)

        # show
        self.stack.set_visible_child_name('countries')

    def _load_subzones_list(self, country):
        # empty
        empty_list(self.subzones_list)

        # back row
        row = BackRow(country.get_name())
        self.subzones_list.add(row)

        # fill
        for subzone in country.get_children():
            if subzone.get_timezone():
                row = ProgressRow(subzone.get_name(), subzone)
                self.subzones_list.add(row)

        # show
        self.stack.set_visible_child_name('subzones')

    ### callbacks ###

    def _on_continent_row_activated(self, list_box, row):
        continent = row.info
        timezone = continent.get_timezone_str()
        if not timezone:
            self._load_countries_list(continent)
        else:
            self.callback(timezone)

    def _on_country_row_activated(self, list_box, row):
        if row.get_name() == 'back_row':
            self.stack.set_visible_child_name('continents')
        else:
            # check if country has timezone
            country = row.info
            timezone = country.get_timezone_str()
            if not timezone:
                self._load_subzones_list(country)
            else:
                self.callback(timezone)

    def _on_subzone_row_activated(self, list_box, row):
        if row.get_name() == 'back_row':
            self.stack.set_visible_child_name('countries')
        else:
            subzone = row.info
            timezone = subzone.get_timezone_str()

            if not subzone:
                print('Subzone', subzone, 'does not have any timezone attached to it! Falling back to UTC.')
                timezone = 'UTC'
            self.callback(timezone)

    ### public methods ###

    def load(self):
        self._load_continents_list()
