# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import GObject
from .global_state import global_state


class Package(GObject.GObject):
    __gtype_name__ = __qualname__

    def __init__(self, package):
        super().__init__()

        self.package = package


### public methods ###
def get_software_suggestions():
    suggestions = []
    software = global_state.get_config('additional_software')
    if software:
        for package in software:
            if ('package' in package and
                'default' in package and
                'name' in package and
                'description' in package and
                    'icon_path' in package):
                suggestions.append(Package(package))
            else:
                print(f'Package {package} not correctly configured!')
    return suggestions
