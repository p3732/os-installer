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
class DeviceRow(Gtk.ListBoxRow):
    __gtype_name__ = 'DeviceRow'

    name_stack = Gtk.Template.Child()
    static_label = Gtk.Template.Child()
    partition_name = Gtk.Template.Child()
    disk_name = Gtk.Template.Child()

    too_small_label = Gtk.Template.Child()

    size = Gtk.Template.Child()
    arrow_stack = Gtk.Template.Child()
    device_path = Gtk.Template.Child()

    def __init__(self, info, too_small, **kwargs):
        super().__init__(**kwargs)

        self.info = info
        self.size.set_label(info.size_text)
        self.device_path.set_label(info.device_path)

        if hasattr(info, 'partitions'):
            self.name_stack.set_visible_child_name('disk')
            if info.name:
                self.disk_name.set_label(info.name)
        else:
            self.name_stack.set_visible_child_name('partition')
            if not info.prefixed:
                info.name = self.partition_name.get_label() + ' ' + info.name
                info.prefixed = True
            self.partition_name.set_label(info.name)

        if too_small:
            self.set_activatable(False)
            self.too_small_label.set_visible(True)
            self.arrow_stack.set_visible_child_name('too_small')
            self.static_label.set_visible(False)
            self._make_light_weight(self.disk_name)
            self._make_light_weight(self.partition_name)

    def _make_light_weight(self, label):
        label.set_label('<span font_weight="light">' + label.get_label() + '</span>')


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/language_row.ui')
class LanguageRow(Adw.ActionRow):
    __gtype_name__ = 'LanguageRow'

    def __init__(self, info, **kwargs):
        super().__init__(**kwargs)

        self.info = info
        self.set_title(info.name)


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/page_wrapper.ui')
class PageWrapper(Gtk.Box):
    __gtype_name__ = 'PageWrapper'

    title = Gtk.Template.Child()
    content = Gtk.Template.Child()

    def __init__(self, page, **kwargs):
        super().__init__(**kwargs)

        self.title.set_label(page.get_name())
        self.content.set_child(page)

    def get_page(self):
        return self.content.get_child()

@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/progress_row.ui')
class ProgressRow(Gtk.ListBoxRow):
    __gtype_name__ = 'ProgressRow'

    label = Gtk.Template.Child()

    def __init__(self, label, additional_info, **kwargs):
        super().__init__(**kwargs)

        self.label.set_label(label)

        self.info = additional_info

    def get_label(self):
        return self.label.get_label()


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/selection_row.ui')
class SelectionRow(Adw.ActionRow):
    __gtype_name__ = 'SelectionRow'

    check_mark_revealer = Gtk.Template.Child()

    def __init__(self, label, additional_info, **kwargs):
        super().__init__(**kwargs)

        self.set_title(label)

        self.info = additional_info

    def get_label(self):
        return self.get_title()

    def set_activated(self, active):
        self.check_mark_revealer.set_reveal_child(active)


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/software_row.ui')
class SoftwareRow(Adw.ActionRow):
    __gtype_name__ = 'SoftwareRow'

    icon = Gtk.Template.Child()
    switch = Gtk.Template.Child()

    def __init__(self, package, **kwargs):
        super().__init__(**kwargs)
        self.set_title(package['name'])
        self.set_subtitle(package['description'])
        self.icon.set_from_file(package['icon_path'])
        self.switch.set_state(package['default'])

        self.package_name = package['package']

    def is_activated(self):
        return self.switch.get_active()

    def set_activated(self, state):
        return self.switch.set_active(state)
