from gi.repository import Gtk


def empty_list(list_box):
    for row in list_box:
        row.destroy()


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/back_row.ui')
class BackRow(Gtk.ListBoxRow):
    __gtype_name__ = 'BackRow'

    label = Gtk.Template.Child()

    def __init__(self, label, additional_info=None, **kwargs):
        super().__init__(**kwargs)

        self.label.set_label(label)

        self.info = additional_info

    def get_info(self):
        return self.info

    def get_label(self):
        return self.label.get_label()


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/disk_row.ui')
class DiskRow(Gtk.ListBoxRow):
    __gtype_name__ = 'DiskRow'

    device_path = Gtk.Template.Child()
    name = Gtk.Template.Child()
    size = Gtk.Template.Child()

    def __init__(self, name, size, device_path, **kwargs):
        super().__init__(**kwargs)

        self.device_path.set_label(device_path)
        self.name.set_label(name)
        self.size.set_label(size)

    def get_device_path(self):
        return self.device_path.get_label()

    def get_disk_name(self):
        return self.name.get_label()

    def get_disk_size(self):
        return self.size.get_label()


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/keyboard_layout_back_row.ui')
class KeyboardLayoutBackRow(Gtk.ListBoxRow):
    __gtype_name__ = 'KeyboardLayoutBackRow'

    label = Gtk.Template.Child()

    def __init__(self, label, additional_info=None, **kwargs):
        super().__init__(**kwargs)

        self.label.set_label(label)

        self.info = additional_info

    def get_info(self):
        return self.info

    def get_label(self):
        return self.label.get_label()


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/partition_row.ui')
class PartitionRow(Gtk.ListBoxRow):
    __gtype_name__ = 'PartitionRow'

    size = Gtk.Template.Child()
    name = Gtk.Template.Child()

    def __init__(self, name, size, device_path, **kwargs):
        super().__init__(**kwargs)

        self.device_path = device_path

        self.name.set_label(name)
        self.size.set_label(size)

    def get_device_path(self):
        return self.device_path

    def get_partition_name(self):
        return self.name.get_label()

    def get_partition_size(self):
        return self.size.get_label()


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/progress_row.ui')
class ProgressRow(Gtk.ListBoxRow):
    __gtype_name__ = 'ProgressRow'

    label = Gtk.Template.Child()

    def __init__(self, label, additional_info, **kwargs):
        super().__init__(**kwargs)

        self.label.set_label(label)

        self.info = additional_info

    def get_info(self):
        return self.info

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

    def get_info(self):
        return self.info

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

    def get_package_name(self):
        return self.package_name

    def is_activated(self):
        return self.switch.get_active()


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/whole_disk_row.ui')
class WholeDiskRow(Gtk.ListBoxRow):
    __gtype_name__ = 'WholeDiskRow'

    size = Gtk.Template.Child()

    def __init__(self, name, size, device_path, **kwargs):
        super().__init__(**kwargs)

        self.size.set_label(size)

        self.name = name
        self.device_path = device_path

    def get_device_path(self):
        return self.device_path

    def get_partition_name(self):
        return self.name

    def get_partition_size(self):
        return self.size.get_label()
