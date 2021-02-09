# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository.GnomeDesktop import XkbInfo


class KeyboardLayoutProvider:
    def __init__(self, global_state):
        self.xkb_info = XkbInfo()

    ### public methods ###

    def get_layouts_for(self, language_short_hand, language):
        layouts = self.xkb_info.get_layouts_for_language(language_short_hand)

        named_layouts = []
        for layout in layouts:
            name = self.xkb_info.get_layout_info(layout).display_name
            named_layouts.append((layout, name))

        # Sort the layouts, prefer those starting with language name or matching language short hand. Then by name.
        return sorted(named_layouts, key=lambda layout:
                      (not layout[1].startswith(language),
                       not layout[0].startswith(language_short_hand),
                       layout[1]))
