from gi.repository import Gtk, Handy

import importlib
import time


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/timezone_window.ui')
class TimezoneWindow(Handy.Window):
    __gtype_name__ = 'TimezoneWindow'

    stack = Gtk.Template.Child()

    timezone_label = Gtk.Template.Child()
    map_placeholder = Gtk.Template.Child()
    confirm_button = Gtk.Template.Child()

    def __init__(self, locale_page, timezone, callback, global_state, **kwargs):
        super().__init__(**kwargs)

        self.map_future_resolved = False
        self.callback = callback
        self.timezone = timezone

        # UI states
        self.set_attached_to(global_state.window)
        self.set_modal(True)
        self.stack.set_visible_child_name('spinner')
        self.timezone_label.set_label(self.timezone)

        # signals
        #self.confirm_button.connect('clicked', self._on_clicked_confirm_button)
        self.confirm_button.connect('clicked', callback)
        self.connect('destroy', self._on_destroy)

        # load map in separate thread
        self.map = global_state.get_future_from(self._load_map, locale_page=locale_page)

    def _load_map(self, locale_page):
        # delayed import
        if not locale_page.TimezoneMap:
            TimezoneMap = importlib.import_module('gi.repository.TimezoneMap', 'TimezoneMap')
            locale_page.TimezoneMap = TimezoneMap
        else:
            TimezoneMap = locale_page.TimezoneMap

        # setup timezone map
        print('imported, timezone', self.timezone)

        map = TimezoneMap.TimezoneMap()
        map.set_size_request(500, 300)
        map.set_timezone(self.timezone)
        map.set_hexpand(True)
        map.set_vexpand(True)

        self.map_placeholder.add(map)
        self.map_placeholder.show_all()

        # signal
        map.connect('location-changed', self._on_map_location_changed)
        self.connect('destroy', self._on_destroy)

        # show
        self.stack.set_visible_child_name('map')

        return map

    def _resolve_map_future(self):
        if not self.map_future_resolved:
            self.map = self.map.result()
            self.map_future_resolved = True

    ### callbacks ###

    def _on_map_location_changed(self, map, object):
        location = map.get_location()
        timezone = location.get_zone()
        self.timezone_label.set_label(timezone)

    def _on_destroy(self, window):
        self._resolve_map_future()
        # TODO is this necessary?
        self.map.destroy()
