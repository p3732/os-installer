# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import GObject
from gi.repository.GnomeDesktop import XkbInfo


class KeyboardInfo(GObject.GObject):
    __gtype_name__ = __qualname__
    name: str
    layout: str

    def __init__(self, name, layout):
        super().__init__()

        self.name = name
        self.layout = layout

def get_layouts_for(language_short_hand, language):
    xkb_info = XkbInfo()
    layouts = xkb_info.get_layouts_for_language(language_short_hand)

    named_layouts = []
    for layout in layouts:
        name = xkb_info.get_layout_info(layout).display_name
        named_layouts.append(KeyboardInfo(name, layout))

    return named_layouts
    # TODO sorting

    # Sort the layouts, prefer those starting with language name or matching language short hand. Then by name.
    return sorted(named_layouts, key=lambda o:
                  (not o.name.startswith(language),
                   not o.layout.startswith(language_short_hand),
                   o.name))
