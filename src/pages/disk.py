from .disk_provider import DiskProvider
from .widgets import DiskRow, PartitionRow

import threading

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/disk.ui')
class DiskPage(Gtk.Box):
    __gtype_name__ = 'DiskPage'

    stack = Gtk.Template.Child()

    disk_list = Gtk.Template.Child()
    partition_list = Gtk.Template.Child()

    disk_label = Gtk.Template.Child()
    disk_size_label = Gtk.Template.Child()

    settings_button = Gtk.Template.Child()
    refresh_button = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        self.global_state = global_state

        self.list_creation_lock = threading.Lock()

        # provider
        self.disk_provider = DiskProvider(global_state)

        # signals
        self.disk_list.connect('row-activated', self._on_disk_row_activated)
        self.partition_list.connect('row-activated', self._on_partition_row_activated)

        self.settings_button.connect('clicked', self._on_clicked_disks_button)
        self.refresh_button.connect('clicked', self.load

    def _setup_disks_list(self):
        # clear list
        self._cleanup_disk_list()

        # fill list
        disks=self.disk_provider.get_disks()
        for name, size, device_path in disks:
            row=DiskRow(name, size, device_path)
            self.disk_list.add(row)

        # show
        self.stack.set_visible_child_name('disks')

    def _setup_partition_list(self, name, size, device_path):
        # clear list
        self._cleanup_partition_list()

        # fill list
        partitions=self.disk_provider.get_partitions(device_path)
        for name, size, device_path in partitions:
            row=PartitionRow(name, size, device_path)
            self.layout_list.add(row)

        # set label
        self.disk_label.set_label(name)
        self.disk_size_label.set_label(size)

        # show
        self.stack.set_visible_child_name('layouts')

    def _cleanup_disk_list(self):
        for row in self.disk_list:
            row.destroy()

    def _cleanup_partition_list(self):
        # remove all but back row and whole disk row
        for row in self.partition_list:
            name=row.get_name()
            if not name == 'back_row' and not name == 'whole_disk_row':
                row.destroy()

    def _continue_with_partition(self, name, size, device_path):
        # TODO
        return

    def _continue_with_disk(self, name, size, device_path):
        # TODO
        return

    ### callbacks ###

    def _on_clicked_disks_button(self, button):
        self.global_state.open_disks()

    def _on_disk_row_activated(self, list_box, row):
        # load partition list if not already loading
        if self.list_creation_lock.aquire(blocking=False):
            name=row.get_disk_name()
            size=row.get_disk_size()
            device_path=row.get_device_path()
            self._setup_partition_list(name, size, device_path)

            self.list_creation_lock.release()

    def _on_partition_row_activated(self, list_box, row):
        if row.get_name() == 'back_row':
            with self.list_creation_lock:
                self.stack.set_visible_child_name('disks')
        else:
            name=row.get_partition_name()
            size=row.get_partition_size()
            device_path=row.get_info()
            if row.get_name() == 'whole_disk_row':
                self._continue_with_disk(name, size, device_path)
            else:
                self._continue_with_partition(name, size, device_path)

    ### public methods ###

    def load(self):
        # reload disk list if not already loading
        if self.list_creation_lock.aquire(blocking=False):
            self._setup_disks_list()
            self.list_creation_lock.release()
