# SPDX-License-Identifier: GPL-3.0-or-later

from .disk_provider import DiskProvider
from .page import Page
from .widgets import DeviceRow, NoPartitionsRow, empty_list

from gi.repository import Gtk
import threading

GIGABYTE_FACTOR = 1024 * 1024 * 1024


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/disk.ui')
class DiskPage(Gtk.Overlay, Page):
    __gtype_name__ = __qualname__
    image_name = 'drive-harddisk-system-symbolic'

    list_stack = Gtk.Template.Child()
    text_stack = Gtk.Template.Child()

    disk_list = Gtk.Template.Child()

    whole_disk_list = Gtk.Template.Child()
    disk_size = Gtk.Template.Child()
    disk_label = Gtk.Template.Child()
    disk_device_path = Gtk.Template.Child()

    partition_list = Gtk.Template.Child()

    settings_button = Gtk.Template.Child()
    refresh_button = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        Gtk.Overlay.__init__(self, **kwargs)

        self.global_state = global_state
        minimum_disk_size = global_state.get_config('minimum_disk_size')
        self.minimum_disk_size = minimum_disk_size * GIGABYTE_FACTOR

        self.current_disk = None

        self.lock = threading.Lock()

        # provider
        self.disk_provider = DiskProvider()

        # signals
        self.disk_list.connect('row-activated', self._on_disk_row_activated)
        self.partition_list.connect('row-activated', self._on_partition_row_activated)
        self.whole_disk_list.connect('row-activated', self._use_whole_disk)

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
        self.list_stack.set_visible_child_name('disks')
        self.text_stack.set_visible_child_name('disks')

    def _setup_partition_list(self, disk_info):
        if self.current_disk == disk_info:
            return
        self.current_disk = disk_info
        # clear list
        empty_list(self.partition_list)

        # efi vars
        if not self.efi_vars_checked:
            self.uses_uefi = self.uses_uefi.result()
            self.efi_vars_checked = True
        disk_uefi_okay = not self.uses_uefi or disk_info.efi_partition

        # set disk info
        self.disk_label.set_label(disk_info.name)
        self.disk_device_path.set_label(disk_info.device_path)
        self.disk_size.set_label(disk_info.size_text)

        # fill list: whole disk row, partitions
        if disk_uefi_okay:
            for partition_info in disk_info.partitions:
                too_small = partition_info.size < self.minimum_disk_size
                row = DeviceRow('partition', partition_info, too_small)
                self.partition_list.add(row)
        else:
            self.partition_list.add(NoPartitionsRow())

        # show
        self.list_stack.set_visible_child_name('partitions')
        self.text_stack.set_visible_child_name('partitions')

    def _store_device_info(self, info):
        self.global_state.set_config('disk_name', info.name)
        self.global_state.set_config('disk_device_path', info.device_path)
        self.global_state.set_config('disk_is_partition', info.is_partition)
        self.global_state.set_config('disk_efi_partition', info.efi_partition)

    ### callbacks ###

    def _on_clicked_disks_button(self, button):
        self.global_state.open_disks()

    def _on_clicked_reload_button(self, button):
        self.load()

    def _on_disk_row_activated(self, list_box, row):
        if not self.lock.acquire(blocking=False):
            return
        self._setup_partition_list(row.info)
        self.can_navigate_backward = True
        self.lock.release()

    def _on_partition_row_activated(self, list_box, row):
        list_box.select_row(row)
        self._store_device_info(row.info)
        self.global_state.advance()

    def _use_whole_disk(self, list_box, row):
        list_box.select_row(row)
        self._store_device_info(self.current_disk)
        self.global_state.advance()

    ### public methods ###

    def load(self):
        if not self.lock.acquire(blocking=False):
            return
        self.can_navigate_backward = False
        self._setup_disk_list()
        self.lock.release()

    def navigate_backward(self):
        self.can_navigate_backward = False
        if not self.lock.acquire(blocking=False):
            return
        self.list_stack.set_visible_child_name('disks')
        self.text_stack.set_visible_child_name('disks')
        self.lock.release()
