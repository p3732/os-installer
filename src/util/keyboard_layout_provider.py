from gi.repository.GnomeDesktop import XkbInfo


class KeyboardLayoutProvider:
    def __init__(self, global_state):
        self.xkb_info = XkbInfo()

    ### public methods ###

    def get_layouts_for(self, language):
        layouts = self.xkb_info.get_layouts_for_language(language)

        named_layouts = []
        for layout in layouts:
            name = self.xkb_info.get_layout_info(layout).display_name
            named_layouts.append((layout, name))

        # sort by name
        return sorted(named_layouts, key=lambda t: t[1])
