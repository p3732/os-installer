# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import GLib, UDisks


class DiskProvider:
    def __init__(self, global_state):
        self.global_state = global_state
        self.udisks_client = None
        self.disks_info = None
        self.partitions_info = None

    def _get_disk_info(self, udisks_object):
        block = udisks_object.get_block()
        drive = self.udisks_client.get_drive_for_block(block)

        if block and drive:
            name = (drive.props.vendor + ' ' + drive.props.model).strip()
            size = self._size_to_str(block.props.size)
            device_path = block.props.device

            return (name, size, device_path)
        else:
            return None

    def _get_partition_info(self, partition_object):
        block = partition_object.get_block()
        partition = partition_object.get_partition()

        if block:
            name = block.props.id_label
            # use number as name
            if name == '':
                name = str(partition.props.number)
            size = self._size_to_str(block.props.size)
            device_path = block.props.device

            return (name, size, device_path)
        else:
            return None

    def _load_udisks_info(self):
        if not self.udisks_client:
            self.udisks_client = UDisks.Client.new_sync()

        # get available devices
        dummy_var = GLib.Variant('a{sv}', None)
        devices = self.udisks_client.get_manager().call_get_block_devices_sync(dummy_var, None)

        # get device information
        self.disks_info = []
        self.partitions_info = {}
        for device in devices:
            udisks_object = self.udisks_client.get_object(device)
            if udisks_object and udisks_object.props.partition_table:
                # disk info
                disk_info = self._get_disk_info(udisks_object)
                if not disk_info:
                    continue
                self.disks_info.append(disk_info)
                disk_device_path = disk_info[2]
                self.partitions_info[disk_device_path] = []

                # partitions info
                partition_table = udisks_object.get_partition_table()
                for partition_name in partition_table.props.partitions:
                    partition_object = self.udisks_client.get_object(partition_name)
                    if partition_object and partition_object.props.partition:
                        partition_info = self._get_partition_info(partition_object)
                        if not partition_info:
                            continue
                        self.partitions_info[disk_device_path].append(partition_info)

    def _size_to_str(self, size):
        return self.udisks_client.get_size_for_display(size, False, False)

    ### public methods ###

    def get_disks(self):
        # always reload information from udisks
        self._load_udisks_info()
        return self.disks_info

    def get_partitions(self, device_path):
        # reuse existing info
        return self.partitions_info[device_path]
