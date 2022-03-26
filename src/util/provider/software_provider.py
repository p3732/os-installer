# SPDX-License-Identifier: GPL-3.0-or-later

from .global_state import global_state


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
                suggestions.append(package)
            else:
                print(f'Package {package} not correctly configured!')
    return suggestions
