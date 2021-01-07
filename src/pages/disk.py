from .disk_provider import DiskProvider
from .widgets import BackRow, DiskRow, PartitionRow, WholeDiskRow

import threading

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/disk.ui')
class DiskPage(Gtk.Box):
    __gtype_name__ = 'DiskPage'

    stack = Gtk.Template.Child()

    disk_list = Gtk.Template.Child()
    partition_list = Gtk.Template.Child()

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
        self.refresh_button.connect('clicked', self._on_clicked_reload_button)

    def _setup_disk_list(self):
        # clear list
        self._cleanup_disk_list()

        # fill list
        disks = self.disk_provider.get_disks()
        for name, size, device_path in disks:
            row = DiskRow(name, size, device_path)
            self.disk_list.add(row)

        # show
        self.stack.set_visible_child_name('disks')

    def _setup_partition_list(self, disk_name, disk_size, disk_device_path):
        # clear list
        self._cleanup_partition_list()

        # fill list
        # back row
        row = BackRow(disk_name)
        self.partition_list.add(row)

        # whole disk row
        row = WholeDiskRow(disk_name, disk_size, disk_device_path)
        self.partition_list.add(row)

        # partition rows
        partitions = self.disk_provider.get_partitions(disk_device_path)
        for name, size, device_path in partitions:
            row = PartitionRow(name, size, device_path)
            self.partition_list.add(row)

        # show
        self.stack.set_visible_child_name('partitions')

    def _cleanup_disk_list(self):
        for row in self.disk_list:
            row.destroy()

    def _cleanup_partition_list(self):
        # remove all but back row and whole disk row
        for row in self.partition_list:
            row.destroy()

    ### callbacks ###

    def _on_clicked_disks_button(self, button):
        self.global_state.open_disks()

    def _on_clicked_reload_button(self, button):
        self.load()

    def _on_disk_row_activated(self, list_box, row):
        # load partition list if not already loading
        if self.list_creation_lock.acquire(blocking=False):
            name = row.get_disk_name()
            size = row.get_disk_size()
            device_path = row.get_device_path()
            self._setup_partition_list(name, size, device_path)

            self.list_creation_lock.release()

    def _on_partition_row_activated(self, list_box, row):
        if row.get_name() == 'back_row':
            with self.list_creation_lock:
                self.stack.set_visible_child_name('disks')
        else:
            list_box.select_row(row)

            # save disk
            is_disk = row.get_name() == 'whole_disk_row'
            name = row.get_partition_name()
            size = row.get_partition_size()
                device_path = row.get_device_path()
            self.global_state.set_disk(name, size, device_path, is_disk)

            self.global_state.advance()

    ### public methods ###

    def load(self):
        # reload disk list if not already loading
        if self.list_creation_lock.acquire(blocking=False):
            self._setup_disk_list()
            self.list_creation_lock.release()
