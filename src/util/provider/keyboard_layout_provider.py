# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import GObject
from gi.repository.GnomeDesktop import XkbInfo


def get_layouts_for(language_short_hand, language):
    xkb_info = XkbInfo()
    layouts = xkb_info.get_layouts_for_language(language_short_hand)

    named_layouts = []
    for layout in layouts:
        o = GObject.GObject()
        o.name = xkb_info.get_layout_info(layout).display_name
        o.layout = layout
        named_layouts.append(o)

    return named_layouts
    # TODO sorting

    # Sort the layouts, prefer those starting with language name or matching language short hand. Then by name.
    return sorted(named_layouts, key=lambda o:
                  (not o.name.startswith(language),
                   not o.layout.startswith(language_short_hand),
                   o.name))
