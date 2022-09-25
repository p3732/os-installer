# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import GObject
from .global_state import global_state


class Package(GObject.GObject):
    __gtype_name__ = __qualname__

    def __init__(self, package, suggested, name, description, icon_path):
        super().__init__()

        self.package = package
        self.suggested = suggested
        self.name = name
        self.description = description
        self.icon_path = icon_path


### public methods ###
def get_software_suggestions():
    if not (software := global_state.get_config('additional_software')):
        return []
    language_code = global_state.get_config('language_code')

    suggestions = []
    for package in software:
        if not 'package' in package:
            print(f'Package {package} not correctly configured!')
            continue

        if (not ((name_key := f'name_{language_code}') in package or
                 (name_key := 'name') in package)):
            # no error if package is only suggested for specific translations
            if not any(key.startswith('name') for key in package.keys()):
                print(f'Package {package} not correctly configured!')
            continue

        suggested = package['suggested'] if 'suggested' in package else False
        name = package[name_key]
        if ((description_key := f'description_{language_code}') in package or
                (description_key := 'description') in package):
            description = package[description_key]
        else:
            description = ''

        icon_path = package['icon_path'] if 'icon_path' in package else ''
        suggestions.append(
            Package(package['package'], suggested, name, description, icon_path))

    return suggestions
