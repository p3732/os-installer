from gi.repository import Gtk, Handy


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/timezone_window.ui')
class TimezoneWindow(Handy.Window):
    __gtype_name__ = 'TimezoneWindow'

    stack = Gtk.Template.Child()

    timezone_label = Gtk.Template.Child()
    map_placeholder = Gtk.Template.Child()
    confirm_button = Gtk.Template.Child()

    def __init__(self, timezone, callback, **kwargs):
        super().__init__(**kwargs)

        self.callback = callback
        self.timezone = timezone

        # UI states
        self.stack.set_visible_child_name('spinner')
        self.timezone_label.set_label(self.timezone)

        # signals
        self.confirm_button.connect('clicked', callback)

    ### callbacks ###

    def _on_map_location_changed(self, map, object):
        location = map.get_location()
        self.timezone = location.get_zone()
        self.timezone_label.set_label(self.timezone)

    ### public methods ###

    def load_map(self, TimezoneMap):
        # setup map
        map = TimezoneMap.TimezoneMap()
        map.set_size_request(600, 300)
        map.set_timezone(self.timezone)
        map.set_hexpand(True)
        map.set_vexpand(True)

        # signal
        map.connect('location-changed', self._on_map_location_changed)

        # show map
        self.map_placeholder.add(map)
        self.map_placeholder.show_all()
        self.stack.set_visible_child_name('map')
