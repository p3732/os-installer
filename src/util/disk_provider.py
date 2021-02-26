# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import GLib, UDisks

EFI_PARTITION_GUID = 'C12A7328-F81F-11D2-BA4B-00A0C93EC93B'
EFI_PARTITON_FLAGS = UDisks.PartitionTypeInfoFlags.SYSTEM.numerator


class DeviceInfo:
    device_path: str
    efi_partition: str
    is_partition: bool = True
    name: str
    size: int
    size_text: str


class DeviceWithTableInfo(DeviceInfo):
    is_gpt: bool
    partitions: list = []

    def __init__(self):
        self.is_partition = False


class DiskProvider:
    def __init__(self):
        self.udisks_client = None

    def _get_one_partition(self, partition, block):
        # partition info
        partition_info = DeviceInfo()
        label = block.props.id_label
        if label == '':
            # no partition name, use number
            partition_info.name = str(partition.props.number)
        else:
            partition_info.name = label
        partition_info.size = block.props.size
        partition_info.size_text = self._size_to_str(partition_info.size)
        partition_info.device_path = block.props.device

        # check if EFI System Partiton
        is_efi_partition = (partition.props.flags == EFI_PARTITON_FLAGS
                            and partition.props.type == EFI_PARTITION_GUID)

        # add to disk info
        return (partition_info, is_efi_partition)

    def _get_partitions(self, partition_table, disk_info):
        partitions = []
        efi_partition = None
        for partition_name in partition_table.props.partitions:
            partition_object = self.udisks_client.get_object(partition_name)
            if partition_object:
                block = partition_object.get_block()
                partition = partition_object.get_partition()
                if block and partition:
                    partition_info, is_efi_partition = self._get_one_partition(partition, block)

                    partitions.append(partition_info)
                    if is_efi_partition:
                        efi_partition = partition_info.device_path
                else:
                    print('Unhandled partiton in partition table, ignoring.')

        # set efi partition
        for partition in partitions:
            partition.efi_partition = efi_partition

        return (partitions, efi_partition)

    def _get_disk_info(self, block, drive, partition_table):
        # disk info
        disk_info = DeviceWithTableInfo()
        disk_info.name = (drive.props.vendor + ' ' + drive.props.model).strip()
        disk_info.size = block.props.size
        disk_info.size_text = self._size_to_str(disk_info.size)
        disk_info.device_path = block.props.device
        disk_info.is_gpt = 'gpt' == partition_table.props.type

        # partitions
        disk_info.partitions, disk_info.efi_partition = self._get_partitions(partition_table, disk_info)

        return disk_info

    def _get_available_disks(self):
        disks = []

        # get available devices
        dummy_var = GLib.Variant('a{sv}', None)
        devices = self.udisks_client.get_manager().call_get_block_devices_sync(dummy_var, None)

        # get device information
        for device in devices:
            udisks_object = self.udisks_client.get_object(device)
            if udisks_object:
                block = udisks_object.get_block()
                partition_table = udisks_object.get_partition_table()
                if block and partition_table:
                    drive = self.udisks_client.get_drive_for_block(block)
                    if drive:
                        disk_info = self._get_disk_info(block, drive, partition_table)
                        disks.append(disk_info)

        return disks

    def _size_to_str(self, size):
        return self.udisks_client.get_size_for_display(size, False, False)

    ### public methods ###

    def get_disks(self):
        if not self.udisks_client:
            self.udisks_client = UDisks.Client.new_sync()

        # get current disks information via udisks
        return self._get_available_disks()
