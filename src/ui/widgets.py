# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk


def reset_model(model, new_values):
    '''
    Reset given model to contain the passed new values.
    (Convenience wrapper)
    '''
    n_prev_items = model.get_n_items()
    model.splice(0, n_prev_items, new_values)

@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/device_row.ui')
class DeviceRow(Adw.ActionRow):
    __gtype_name__ = 'DeviceRow'

    stack = Gtk.Template.Child()
    size = Gtk.Template.Child()

    def __init__(self, info, too_small=False, **kwargs):
        super().__init__(**kwargs)

        self.info = info
        self.size.set_label(info.size_text)
        if info.name:
            self.set_title(info.name)

        self.set_subtitle(info.device_path)

        if too_small:
            self.set_activatable(False)
            self.set_sensitive(False)
            self.stack.set_visible_child_name('too_small')


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/page_wrapper.ui')
class PageWrapper(Gtk.Box):
    __gtype_name__ = 'PageWrapper'

    content = Gtk.Template.Child()

    def __init__(self, page, **kwargs):
        super().__init__(**kwargs)

        self.content.set_child(page)

    def get_page(self):
        return self.content.get_child()

@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/progress_row.ui')
class ProgressRow(Adw.ActionRow):
    __gtype_name__ = 'ProgressRow'

    def __init__(self, label, additional_info, **kwargs):
        super().__init__(**kwargs)

        self.set_title(label)

        self.info = additional_info

    def get_label(self):
        return self.get_title()


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/selection_row.ui')
class SelectionRow(Adw.ActionRow):
    __gtype_name__ = 'SelectionRow'

    icon = Gtk.Template.Child()
    switch = Gtk.Template.Child()

    def __init__(self, title, description, icon_path, default_state, info,
                 fallback_icon, **kwargs):
        super().__init__(**kwargs)
        self.set_title(title)
        self.set_subtitle(description)
        self.switch.set_state(default_state)
        if not icon_path:
            self.icon.set_from_icon_name(fallback_icon)
            self.icon.set_icon_size(Gtk.IconSize.LARGE)
        else:
            self.icon.set_from_file(icon_path)

        self.info = info

    def is_activated(self):
        return self.switch.get_active()

    def set_activated(self, state):
        return self.switch.set_active(state)
