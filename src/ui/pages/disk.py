# SPDX-License-Identifier: GPL-3.0-or-later

from threading import Lock

from gi.repository import Gio, Gtk

from .disk_provider import disk_provider
from .global_state import global_state
from .installation_scripting import installation_scripting, Step
from .page import Page
from .system_calls import is_booted_with_uefi, open_disks
from .widgets import reset_model, DeviceRow

GIGABYTE_FACTOR = 1024 * 1024 * 1024


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/disk.ui')
class DiskPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    no_disk_image_name = 'no-disk-symbolic'
    default_image_name = 'drive-harddisk-system-symbolic'
    image_name = default_image_name
    can_reload = True

    disk_label = Gtk.Template.Child()
    disk_list = Gtk.Template.Child()
    disk_size = Gtk.Template.Child()
    list_stack = Gtk.Template.Child()
    missing_things_info = Gtk.Template.Child()
    partition_list = Gtk.Template.Child()
    whole_disk_row = Gtk.Template.Child()

    disk_list_model = Gio.ListStore()
    partition_list_model = Gio.ListStore()

    current_disk = None
    lock = Lock()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        self.minimum_disk_size = global_state.get_config('minimum_disk_size') * GIGABYTE_FACTOR

        # models
        self.disk_list.bind_model(self.disk_list_model, self._create_device_row)
        self.partition_list.bind_model(self.partition_list_model, self._create_device_row)

    def _create_device_row(self, info):
        too_small = info.size < self.minimum_disk_size
        return DeviceRow(info, too_small)

    def _setup_disk_list(self):
        if global_state.demo_mode:
            disks = disk_provider.get_testing_dummy_disks()
        else:
            disks = disk_provider.get_disks()
        if len(disks) == 0:
            self.list_stack.set_visible_child_name('no-disks')
            self.image_name = self.no_disk_image_name
        else:
            reset_model(self.disk_list_model, disks)
            self.list_stack.set_visible_child_name('disks')
            self.image_name = self.default_image_name
        global_state.set_title_image(self.image_name)

    def _setup_partition_list(self, disk_info):
        self.current_disk = disk_info

        # set disk info
        self.disk_label.set_label(disk_info.name)
        self.whole_disk_row.set_subtitle(disk_info.device_path)
        self.disk_size.set_label(disk_info.size_text)

        # reset partition list
        list_partitions = (len(disk_info.partitions) > 0 and
                           (not is_booted_with_uefi() or not disk_info.efi_partition is None))
        self.missing_things_info.set_visible(not list_partitions)
        reset_model(self.partition_list_model,
                    disk_info.partitions if list_partitions else [])

        # show
        self.list_stack.set_visible_child_name('partitions')

    def _store_device_info(self, info):
        global_state.set_config('disk_name', info.name)
        global_state.set_config('disk_device_path', info.device_path)
        global_state.set_config('disk_is_partition', not type(info) == type(self.current_disk))
        global_state.set_config('disk_efi_partition', self.current_disk.efi_partition)

    ### callbacks ###

    @Gtk.Template.Callback('clicked_disks_button')
    def _clicked_disks_button(self, button):
        open_disks()

    @Gtk.Template.Callback('disk_selected')
    def _disk_selected(self, list_box, row):
        with self.lock:
            self._setup_partition_list(row.info)
            self.can_navigate_backward = True

    @Gtk.Template.Callback('use_partition')
    def _use_partition(self, list_box, row):
        self._store_device_info(row.info)
        global_state.advance(self)

    @Gtk.Template.Callback('use_whole_disk')
    def _use_whole_disk(self, list_box, row):
        self._store_device_info(self.current_disk)
        global_state.advance(self)

    ### public methods ###

    def load(self):
        if not self.loaded:
            self.loaded = True
            # start prepare script
            installation_scripting.set_ok_to_start_step(Step.prepare)

        with self.lock:
            self._setup_disk_list()

    def unload(self):
        self.can_navigate_backward = False

    def navigate_backward(self):
        with self.lock:
            self.can_navigate_backward = False
            self.list_stack.set_visible_child_name('disks')
