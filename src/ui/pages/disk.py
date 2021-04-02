# SPDX-License-Identifier: GPL-3.0-or-later

from threading import Lock

from gi.repository import Gtk

from .disk_provider import disk_provider
from .global_state import global_state
from .installation_scripting import installation_scripting
from .page import Page
from .system_calls import has_efi_vars, open_disks
from .widgets import DeviceRow, NoPartitionsRow, empty_list

GIGABYTE_FACTOR = 1024 * 1024 * 1024


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/disk.ui')
class DiskPage(Gtk.Box, Page):
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

    current_disk = None
    lock = Lock()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        self.minimum_disk_size = global_state.get_config('minimum_disk_size') * GIGABYTE_FACTOR

        # signals
        self.disk_list.connect('row-activated', self._on_disk_row_activated)
        self.partition_list.connect('row-activated', self._on_partition_row_activated)
        self.whole_disk_list.connect('row-activated', self._use_whole_disk)

        self.settings_button.connect('clicked', self._on_clicked_disks_button)
        self.refresh_button.connect('clicked', self._on_clicked_reload_button)

        # start gl checking
        self.uses_uefi = has_efi_vars()

    def _setup_disk_list(self):
        # clear list
        empty_list(self.disk_list)

        # fill list
        disks = disk_provider.get_disks()
        for disk_info in disks:
            too_small = disk_info.size < self.minimum_disk_size
            row = DeviceRow('disk', disk_info, too_small)
            self.disk_list.add(row)

        # show
        self.list_stack.set_visible_child_name('disks')

    def _setup_partition_list(self, disk_info):
        self.current_disk = disk_info

        empty_list(self.partition_list)

        # efi vars
        disk_uefi_okay = not self.uses_uefi or disk_info.efi_partition

        # set disk info
        self.disk_label.set_label(disk_info.name)
        self.disk_device_path.set_label(disk_info.device_path)
        self.disk_size.set_label(disk_info.size_text)

        # fill partition list
        if disk_uefi_okay:
            for partition_info in disk_info.partitions:
                too_small = partition_info.size < self.minimum_disk_size
                row = DeviceRow('partition', partition_info, too_small)
                self.partition_list.add(row)
        else:
            self.partition_list.add(NoPartitionsRow())

        # show
        self.list_stack.set_visible_child_name('partitions')

    def _store_device_info(self, info):
        global_state.set_config('disk_name', info.name)
        global_state.set_config('disk_device_path', info.device_path)
        global_state.set_config('disk_is_partition', info.is_partition)
        global_state.set_config('disk_efi_partition', info.efi_partition)

    ### callbacks ###

    def _on_clicked_disks_button(self, button):
        open_disks()

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
        global_state.advance(self.__gtype_name__)

    def _use_whole_disk(self, list_box, row):
        list_box.select_row(row)
        self._store_device_info(self.current_disk)
        global_state.advance(self.__gtype_name__)

    ### public methods ###

    def load_once(self):
        # start prepare script
        installation_scripting.start_next_step()

        with self.lock:
            self._setup_disk_list()

    def navigate_backward(self):
        self.can_navigate_backward = False
        if not self.lock.acquire(blocking=False):
            return
        self.list_stack.set_visible_child_name('disks')
        self.text_stack.set_visible_child_name('disks')
        self.lock.release()
