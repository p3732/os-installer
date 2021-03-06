# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import GLib, GObject, UDisks

EFI_PARTITION_GUID = 'C12A7328-F81F-11D2-BA4B-00A0C93EC93B'
EFI_PARTITON_FLAGS = UDisks.PartitionTypeInfoFlags.SYSTEM.numerator


class DeviceInfo:
    device_path: str
    name: str
    prefixed: bool = False
    size: int
    size_text: str


class Disk(DeviceInfo):
    has_table: bool = False
    is_msdos: bool = False
    is_gpt: bool = False
    partitions: list = []
    efi_partition: str = ''


class DiskProvider:
    udisks_client = UDisks.Client.new_sync()

    def _get_one_partition(self, partition, block):
        # partition info
        partition_info = DeviceInfo()
        partition_info.name = block.props.id_label
        if partition_info.name == '':
            partition_info.name = str(partition.props.number)
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
        efi_partition = ''
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

        return (partitions, efi_partition)

    def _get_disk_info(self, block, drive, partition_table):
        # disk info
        disk_info = Disk()
        disk_info.name = (drive.props.vendor + ' ' + drive.props.model).strip()
        disk_info.size = block.props.size
        disk_info.size_text = self._size_to_str(disk_info.size)
        disk_info.device_path = block.props.device

        # partitions
        if partition_table:
            disk_info.has_table = True
            disk_info.is_gpt = 'gpt' == partition_table.props.type
            disk_info.is_msdos = 'msdos' == partition_table.props.type
            disk_info.partitions, disk_info.efi_partition = self._get_partitions(partition_table, disk_info)

        return disk_info

    def _size_to_str(self, size):
        return self.udisks_client.get_size_for_display(size, False, False)

    ### public methods ###

    def get_disks(self):
        disks = []

        # get available devices
        dummy_var = GLib.Variant('a{sv}', None)
        devices = self.udisks_client.get_manager().call_get_block_devices_sync(dummy_var, None)

        # get device information
        for device in devices:
            udisks_object = self.udisks_client.get_object(device)
            if udisks_object:
                partition = udisks_object.get_partition()
                if partition:
                    continue  # skip partitions

                block = udisks_object.get_block()
                partition_table = udisks_object.get_partition_table()
                if block:
                    drive = self.udisks_client.get_drive_for_block(block)
                    if drive and drive.props.size > 0 and not drive.props.optical:
                        disk_info = self._get_disk_info(block, drive, partition_table)
                        disks.append(disk_info)

        return disks


disk_provider = DiskProvider()
