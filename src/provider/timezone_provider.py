# SPDX-License-Identifier: GPL-3.0-or-later

from time import time
from gi.repository import GnomeDesktop, GObject, GWeather


class Timezone(GObject.GObject):
    __gtype_name__ = __qualname__

    def __init__(self, name):
        super().__init__()

        self.name: str = name
        self.lower_case_name: str = name.lower()
        self.locations: set = set()


def _get_location_children(location):
    # this code is un-pythonesque because libgweather decided to simplify their API too much
    first_child = location.next_child(None)
    if not first_child:
        return []
    children = [first_child]
    while child := location.next_child(children[-1]):
        children.append(child)
    return children


def _add_all_locations_to_timezone(timezone, location):
    for child in _get_location_children(location):
        timezone.locations.add(child.get_name().lower())
        _add_all_locations_to_timezone(timezone, child)


def _recurse_location(location, timezones):
    for child in _get_location_children(location):
        if child.has_timezone():
            timezone_id = child.get_timezone().get_identifier()
            if not timezone_id in timezones:
                print(f'Developer hint: Unknown timezone {timezone_id} {child.get_name()}')
                continue
            _add_all_locations_to_timezone(timezones[timezone_id], child)
        else:
            _recurse_location(child, timezones)


### public methods ###

def get_current_timezone():
    timezone = GnomeDesktop.WallClock().get_timezone()
    return timezone.get_identifier()


def get_timezones():
    timezones = {timezone.get_identifier(): Timezone(timezone.get_identifier())
                 for timezone in GWeather.Location().get_world().get_timezones()}
    for child in _get_location_children(GWeather.Location().get_world()):
        if not child.has_timezone(): # skips UTC and Etc/GMT+12
            _recurse_location(child, timezones)

    return sorted(timezones.values(), key=lambda t: t.name)
