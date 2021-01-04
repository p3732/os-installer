class DiskProvider:
    def __init__(self, global_state):
        self.global_state = global_state

    ### public methods ###

    def get_disks(self):
        # TODO use UDisks?
        # sudo lsblk -PSoNAME,MODEL,SIZE
        disks = [('Disk Example', '1.3 Tb', '/dev/sda')]

        return disks

    def get_partitions(self, device_path):
        # TODO
        partitions = [('Partition 1', '150 Gb', '/dev/sda1'),
                      ('Partition 2', '250 Gb', '/dev/sda2'), ]

        return partitions
