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


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/disk_row.ui')
class DiskRow(Gtk.ListBoxRow):
    __gtype_name__ = 'DiskRow'

    device_path = Gtk.Template.Child()
    name = Gtk.Template.Child()
    size = Gtk.Template.Child()

    def __init__(self, info, **kwargs):
        super().__init__(**kwargs)

        self.info = info
        if info.name:
            self.name.set_label(info.name)
        else:
            info.name = self.name.get_label()
        self.size.set_label(info.size_text)
        self.device_path.set_label(info.device_path)


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/disk_too_small_row.ui')
class DiskTooSmallRow(Gtk.ListBoxRow):
    __gtype_name__ = 'DiskTooSmallRow'

    device_path = Gtk.Template.Child()
    name = Gtk.Template.Child()
    size = Gtk.Template.Child()

    def __init__(self, info, **kwargs):
        super().__init__(**kwargs)

        if info.name:
            self.name.set_label(info.name)
        self.size.set_label(info.size_text)
        self.device_path.set_label(info.device_path)


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/disk_back_row.ui')
class DiskBackRow(Gtk.ListBoxRow):
    __gtype_name__ = 'DiskBackRow'

    label = Gtk.Template.Child()

    def __init__(self, label, **kwargs):
        super().__init__(**kwargs)

        self.label.set_label(label)


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/keyboard_layout_back_row.ui')
class KeyboardLayoutBackRow(Gtk.ListBoxRow):
    __gtype_name__ = 'KeyboardLayoutBackRow'

    label = Gtk.Template.Child()

    def __init__(self, label, additional_info=None, **kwargs):
        super().__init__(**kwargs)

        self.label.set_label(label)

        self.info = additional_info

    def get_label(self):
        return self.label.get_label()


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/language_row.ui')
class LanguageRow(Gtk.ListBoxRow):
    __gtype_name__ = 'LanguageRow'

    label = Gtk.Template.Child()

    def __init__(self, label, additional_info=None, **kwargs):
        super().__init__(**kwargs)

        self.label.set_label(label)

        self.info = additional_info

    def get_label(self):
        return self.label.get_label()


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/partition_row.ui')
class PartitionRow(Gtk.ListBoxRow):
    __gtype_name__ = 'PartitionRow'

    size = Gtk.Template.Child()
    name = Gtk.Template.Child()
    device_path = Gtk.Template.Child()

    def __init__(self, info, **kwargs):
        super().__init__(**kwargs)

        self.info = info

        new_name = self.name.get_label() + ' ' + info.name
        self.name.set_label(new_name)
        self.size.set_label(info.size_text)
        self.device_path.set_label(info.device_path)

    def get_device_name(self):
        return self.name.get_label()


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/partition_too_small_row.ui')
class PartitionTooSmallRow(Gtk.ListBoxRow):
    __gtype_name__ = 'PartitionTooSmallRow'

    size = Gtk.Template.Child()
    name = Gtk.Template.Child()
    device_path = Gtk.Template.Child()

    def __init__(self, info, **kwargs):
        super().__init__(**kwargs)

        new_name = self.name.get_label() + ' ' + info.name
        self.name.set_label(new_name)
        self.size.set_label(info.size_text)
        self.device_path.set_label(info.device_path)


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
    check_mark = Gtk.Template.Child()

    def __init__(self, label, additional_info, **kwargs):
        super().__init__(**kwargs)

        self.label.set_label(label)

        self.info = additional_info

    def get_label(self):
        return self.label.get_label()

    def set_activated(self, active):
        self.check_mark.set_visible(active)


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


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/whole_disk_row.ui')
class WholeDiskRow(Gtk.ListBoxRow):
    __gtype_name__ = 'WholeDiskRow'

    size = Gtk.Template.Child()
    device_path = Gtk.Template.Child()

    def __init__(self, info, **kwargs):
        super().__init__(**kwargs)

        self.info = info

        self.size.set_label(info.size_text)
        self.device_path.set_label(info.device_path)

    def get_device_name(self):
        return self.info.name
