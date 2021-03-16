# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository.GnomeDesktop import XkbInfo


def get_layouts_for(language_short_hand, language):
    xkb_info = XkbInfo()
    layouts = xkb_info.get_layouts_for_language(language_short_hand)

    named_layouts = []
    for layout in layouts:
        name = xkb_info.get_layout_info(layout).display_name
        named_layouts.append((layout, name))

    # Sort the layouts, prefer those starting with language name or matching language short hand. Then by name.
    return sorted(named_layouts, key=lambda layout:
                  (not layout[1].startswith(language),
                   not layout[0].startswith(language_short_hand),
                   layout[1]))
