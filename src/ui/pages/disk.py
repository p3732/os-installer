# SPDX-License-Identifier: GPL-3.0-or-later

from threading import Lock

from gi.repository import Gio, Gtk

from .disk_provider import disk_provider
from .global_state import global_state
from .installation_scripting import installation_scripting, Step
from .page import Page
from .system_calls import is_booted_with_uefi, open_disks
from .widgets import DeviceRow, NoPartitionsRow

GIGABYTE_FACTOR = 1024 * 1024 * 1024


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/disk.ui')
class DiskPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'drive-harddisk-system-symbolic'
    can_reload = True

    list_stack = Gtk.Template.Child()
    text_stack = Gtk.Template.Child()

    disk_list = Gtk.Template.Child()
    disk_list_model = Gio.ListStore()

    whole_disk_list = Gtk.Template.Child()
    disk_size = Gtk.Template.Child()
    disk_label = Gtk.Template.Child()
    disk_device_path = Gtk.Template.Child()

    partition_list = Gtk.Template.Child()
    partition_list_model = Gio.ListStore()

    settings_button = Gtk.Template.Child()

    current_disk = None
    lock = Lock()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        self.minimum_disk_size = global_state.get_config('minimum_disk_size') * GIGABYTE_FACTOR

        # signals
        self.disk_list.connect('row-activated', self._on_disk_row_activated)
        self.partition_list.connect('row-activated', self._on_partition_row_activated)
        self.whole_disk_list.connect('row-activated', self._use_whole_disk)

        # models
        self.disk_list.bind_model(self.disk_list_model, lambda x: x)
        self.partition_list.bind_model(self.partition_list_model, lambda x: x)

        self.settings_button.connect('clicked', self._on_clicked_disks_button)

    def _set_stacks(self, state):
        self.list_stack.set_visible_child_name(state)
        self.text_stack.set_visible_child_name(state)

    def _setup_disk_list(self):
        # fill list
        disk_rows = []
        for disk_info in disk_provider.get_disks():
            too_small = disk_info.size < self.minimum_disk_size
            disk_rows.append(DeviceRow(disk_info, too_small))

        n_items = self.disk_list_model.get_n_items()
        self.disk_list_model.splice(0, n_items, disk_rows)

        # show
        self._set_stacks('disks')

    def _setup_partition_list(self, disk_info):
        self.current_disk = disk_info

        # set disk info
        self.disk_label.set_label(disk_info.name)
        self.disk_device_path.set_label(disk_info.device_path)
        self.disk_size.set_label(disk_info.size_text)

        # fill partition list
        partition_rows = []
        disk_uefi_okay = not is_booted_with_uefi() or disk_info.efi_partition
        if disk_uefi_okay and len(disk_info.partitions) > 0:
            for partition_info in disk_info.partitions:
                too_small = partition_info.size < self.minimum_disk_size
                partition_rows.append(DeviceRow(partition_info, too_small))
        else:
            partition_rows = [NoPartitionsRow()]

        n_items = self.partition_list_model.get_n_items()
        self.partition_list_model.splice(0, n_items, partition_rows)

        # show
        self._set_stacks('partitions')

    def _store_device_info(self, info):
        global_state.set_config('disk_name', info.name)
        global_state.set_config('disk_device_path', info.device_path)
        global_state.set_config('disk_is_partition', not type(info) == type(self.current_disk))
        global_state.set_config('disk_efi_partition', self.current_disk.efi_partition)

    ### callbacks ###

    def _on_clicked_disks_button(self, button):
        open_disks()

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

    def load(self):
        if not self.loaded:
            self.loaded = True
            # start prepare script
            installation_scripting.set_ok_to_start_step(Step.prepare)

        with self.lock:
            self._setup_disk_list()

    def navigate_backward(self):
        self.can_navigate_backward = False
        if not self.lock.acquire(blocking=False):
            return

        self._set_stacks('disks')
        self.lock.release()
