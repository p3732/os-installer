# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk
import threading
from .disk_provider import DiskProvider
from .widgets import DeviceRow, DiskBackRow, NoPartitionsRow, empty_list


GIGABYTE_FACTOR = 1024 * 1024 * 1024


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
        minimum_disk_size = global_state.get_config('minimum_disk_size')
        self.minimum_disk_size = minimum_disk_size * GIGABYTE_FACTOR

        self.list_creation_lock = threading.Lock()

        # provider
        self.disk_provider = DiskProvider()

        # signals
        self.disk_list.connect('row-activated', self._on_disk_row_activated)
        self.partition_list.connect('row-activated', self._on_partition_row_activated)

        self.settings_button.connect('clicked', self._on_clicked_disks_button)
        self.refresh_button.connect('clicked', self._on_clicked_reload_button)

        # start gl checking
        self.efi_vars_checked = False
        self.uses_uefi = global_state.has_efi_vars()

    def _setup_disk_list(self):
        # clear list
        empty_list(self.disk_list)

        # fill list
        disks = self.disk_provider.get_disks()
        for disk_info in disks:
            too_small = disk_info.size < self.minimum_disk_size
            row = DeviceRow('disk', disk_info, too_small)
            self.disk_list.add(row)

        # show
        self.stack.set_visible_child_name('disks')

    def _setup_partition_list(self, disk_info):
        # clear list
        empty_list(self.partition_list)

        # efi vars
        if not self.efi_vars_checked:
            self.uses_uefi = self.uses_uefi.result()
            self.efi_vars_checked = True
        disk_uefi_okay = not self.uses_uefi or disk_info.efi_partition

        # fill list: back row, whole disk row, partitions
        self.partition_list.add(DiskBackRow(disk_info.name))
        self.partition_list.add(DeviceRow('whole_disk', disk_info, False))
        if disk_uefi_okay:
            for partition_info in disk_info.partitions:
                too_small = partition_info.size < self.minimum_disk_size
                row = DeviceRow('partition', partition_info, too_small)
                self.partition_list.add(row)
        else:
            self.partition_list.add(NoPartitionsRow())

    ### callbacks ###

    def _on_clicked_disks_button(self, button):
        self.global_state.open_disks()

    def _on_clicked_reload_button(self, button):
        self.load()

    def _on_disk_row_activated(self, list_box, row):
        # load partition list if not already loading
        if self.list_creation_lock.acquire(blocking=False):
            self._setup_partition_list(row.info)
            self.stack.set_visible_child_name('partitions')

            self.list_creation_lock.release()

    def _on_partition_row_activated(self, list_box, row):
        if row.get_name() == 'back_row':
            with self.list_creation_lock:
                self.stack.set_visible_child_name('disks')
        else:
            list_box.select_row(row)

            self.global_state.set_config('disk_name', row.info.name)
            self.global_state.set_config('disk_device_path', row.info.device_path)
            self.global_state.set_config('disk_is_partition', row.info.is_partition)
            self.global_state.set_config('disk_efi_partition', row.info.efi_partition)

            self.global_state.advance()

    ### public methods ###

    def load(self):
        # reload disk list if not already loading
        if self.list_creation_lock.acquire(blocking=False):
            self._setup_disk_list()
            self.list_creation_lock.release()
