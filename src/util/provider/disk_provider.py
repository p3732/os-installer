# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import GLib, GObject

class DeviceInfo(GObject.GObject):
    __gtype_name__ = __qualname__

    name: str = None
    size: int
    size_text: str
    device_path: str

    def __init__(self, name, size, size_text, device_path):
        super().__init__()

        if name:
            self.name = name.strip()
        self.size = size
        self.size_text = size_text
        self.device_path = device_path


class Disk(DeviceInfo):
    partitions: list = []
    efi_partition: str = ''

    def __init__(self, name, size, size_text, device_path, partitions=None):
        super().__init__(name, size, size_text, device_path)

        if partitions:
            self.partitions, self.efi_partition = partitions

class DiskProvider:
    udisks_client = None

    EFI_PARTITION_GUID = 'C12A7328-F81F-11D2-BA4B-00A0C93EC93B'
    EFI_PARTITON_FLAGS = None

    def _init_client(self):
        # avoids initializing udisks client in demo mode
        import gi                           # noqa: E402
        gi.require_version('UDisks', '2.0') # noqa: E402
        from gi.repository import UDisks
        self.EFI_PARTITON_FLAGS = UDisks.PartitionTypeInfoFlags.SYSTEM.numerator
        self.udisks_client = UDisks.Client.new_sync()

    def _get_one_partition(self, partition, block):
        # partition info
        partition_info = DeviceInfo(
            name=block.props.id_label,
            size=block.props.size,
            size_text=self._size_to_str(block.props.size),
            device_path=block.props.device)

        # check if EFI System Partiton
        is_efi_partition = (partition.props.flags == self.EFI_PARTITON_FLAGS
                            and partition.props.type == EFI_PARTITION_GUID)

        # add to disk info
        return (partition_info, is_efi_partition)

    def _get_partitions(self, partition_table):
        if not partition_table:
            return None

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
        disk = Disk(
            name=drive.props.vendor + ' ' + drive.props.model,
            size=block.props.size,
            size_text=self._size_to_str(block.props.size),
            device_path=block.props.device,
            partitions=self._get_partitions(partition_table))

        return disk

    def _size_to_str(self, size):
        return self.udisks_client.get_size_for_display(size, False, False)

    ### public methods ###

    def get_disks(self):
        if not self.udisks_client:
            self._init_client()
        
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

    def get_testing_dummy_disks(self):
        self.flip = not self.flip if hasattr(self, 'flip') and self.flip else True
        if not self.flip:
            return []
        smol_partition = DeviceInfo("sm0l partiton", 1000, "1 KB", "/dev/00null")
        smol_disk = Disk("Dummy", 10000, "/dev/null", "10 KB", ([smol_partition], None))

        efi_partition = DeviceInfo("EFI", 200000000, "20 GB", "/dev/sda_efi")
        unnamed_partition_1 = DeviceInfo(None, 20000000000, "20 GB", "/dev/sda_unnamed")
        unnamed_partition_2 = DeviceInfo(None, 20000000000, "20 GB", "/dev/sda_unnamed2")
        unnamed_partition_3 = DeviceInfo(None, 20000000000, "20 GB", "/dev/sda_unnamed3")
        partytion = DeviceInfo("PARTYtion", 20000000000, "20 GB", "/dev/sda_party")
        disk = Disk("Totally real device", 100000000000, "100 GB", "/dev/sda", ([efi_partition, partytion, unnamed_partition_1, unnamed_partition_2, unnamed_partition_3], "EFI"))

        unformated_big_disk = Disk("VERY BIG DISK", 1000000000000000, "1000 TB", "/dev/sdb_very_big")

        return [smol_disk, disk, unformated_big_disk]


disk_provider = DiskProvider()
