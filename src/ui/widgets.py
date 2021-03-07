# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk


def empty_list(list_box):
    for row in list_box:
        row.destroy()


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/back_row.ui')
class BackRow(Gtk.ListBoxRow):
    __gtype_name__ = 'BackRow'

    label = Gtk.Template.Child()

    def __init__(self, text, additional_info=None, **kwargs):
        super().__init__(**kwargs)

        self.label.set_label(text)
        self.info = additional_info

    def get_text(self):
        return self.label.get_label()


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

    def __init__(self, row_type, info, too_small, **kwargs):
        super().__init__(**kwargs)

        self.info = info
        self.size.set_label(info.size_text)
        self.device_path.set_label(info.device_path)

        self.name_stack.set_visible_child_name(row_type)
        if 'disk' == row_type:
            if info.name:
                self.disk_name.set_label(info.name)
        elif 'partition' == row_type:
            if not info.prefixed:
                info.name = self.partition_name.get_label() + ' ' + info.name
                info.prefixed = True
            self.partition_name.set_label(info.name)

        if too_small:
            self.set_activatable(False)
            self.too_small_label.set_visible(True)
            self.arrow_stack.set_visible_child_name('too_small')
            self._make_light_weight(self.static_label)
            self._make_light_weight(self.disk_name)
            self._make_light_weight(self.partition_name)

    def _make_light_weight(self, label):
        label.set_label('<span font_weight="light">' + label.get_label() + '</span>')


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/language_row.ui')
class LanguageRow(Gtk.ListBoxRow):
    __gtype_name__ = 'LanguageRow'

    label = Gtk.Template.Child()

    def __init__(self, info, **kwargs):
        super().__init__(**kwargs)

        self.info = info
        self.label.set_label(info.name)


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/no_partitions_row.ui')
class NoPartitionsRow(Gtk.ListBoxRow):
    __gtype_name__ = 'NoPartitionsRow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


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
class SelectionRow(Gtk.ListBoxRow):
    __gtype_name__ = 'SelectionRow'

    label = Gtk.Template.Child()
    check_mark_revealer = Gtk.Template.Child()

    def __init__(self, label, additional_info, **kwargs):
        super().__init__(**kwargs)

        self.label.set_label(label)

        self.info = additional_info

    def get_label(self):
        return self.label.get_label()

    def set_activated(self, active):
        self.check_mark_revealer.set_reveal_child(active)


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/software_row.ui')
class SoftwareRow(Gtk.ListBoxRow):
    __gtype_name__ = 'SoftwareRow'

    icon = Gtk.Template.Child()
    name_label = Gtk.Template.Child()
    description_label = Gtk.Template.Child()
    switch = Gtk.Template.Child()

    def __init__(self, name, description, package_name, default=False, icon_path='', **kwargs):
        super().__init__(**kwargs)

        self.name_label.set_label(name)
        self.description_label.set_label(description)
        self.icon.set_from_file(icon_path)
        self.switch.set_state(default)

        self.package_name = package_name

    def is_activated(self):
        return self.switch.get_active()

    def set_activated(self, state):
        return self.switch.set_active(state)
