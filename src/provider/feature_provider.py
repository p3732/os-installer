# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import GObject
from .global_state import global_state


class Feature(GObject.GObject):
    __gtype_name__ = __qualname__

    def __init__(self, feature, suggested, name, description, icon_path):
        super().__init__()

        self.feature = feature
        self.suggested = suggested
        self.name = name
        self.description = description
        self.icon_path = icon_path


### public methods ###
def get_feature_suggestions():
    if not (features := global_state.get_config('additional_features')):
        return []
    language_code = global_state.get_config('language_code')

    suggestions = []
    for feature in features:
        if not 'feature' in feature:
            print(f'feature {feature} not correctly configured!')
            continue

        if (not ((name_key := f'name_{language_code}') in feature or
                 (name_key := 'name') in feature)):
            # no error if feature is only suggested for specific translations
            if not any(key.startswith('name') for key in feature.keys()):
                print(f'feature {feature} not correctly configured!')
            continue

        suggested = feature['suggested'] if 'suggested' in feature else False
        name = feature[name_key]
        if ((description_key := f'description_{language_code}') in feature or
                (description_key := 'description') in feature):
            description = feature[description_key]
        else:
            description = ''

        icon_path = feature['icon_path'] if 'icon_path' in feature else ''
        suggestions.append(
            Feature(feature['feature'], suggested, name, description, icon_path))

    return suggestions
