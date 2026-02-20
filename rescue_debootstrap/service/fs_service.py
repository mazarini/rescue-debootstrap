from rescue_debootstrap.model.disk import Disk
from rescue_debootstrap.model.disk_model import DiskModelSpec
from rescue_debootstrap.model.partition import Partition
from rescue_debootstrap.model.storage_group import StorageGroup
from rescue_debootstrap.util.command import CMD


class FsService:
    def create_fs(self, storage_groups: list[StorageGroup]):
        for storage in storage_groups:
            for partition in storage.partitions:
                match partition.type:
                    case "efi":
                        self.mkfs(storage.disk_model, storage.disks, partition)
                    case "ext4":
                        self.mkfs(storage.disk_model, storage.disks, partition)
                    case "linux-swap":
                        self.mkfs(storage.disk_model, storage.disks, partition)

    def mkfs(self, disk_model: DiskModelSpec, disks: list[Disk], partition: Partition):
        for disk in disks:
            if len(disks) > 1:
                label = f"{partition.label}-{disk.number}"
            else:
                label = partition.label
            device = partition.device(disk_model, disk)
            match partition.type:
                case "efi":
                    CMD.sh(f"mkfs.fat -F 32 -n {label} {device}")
                case "ext4":
                    CMD.sh(f"mkfs.ext4 -L {label} {device}")
                case "linux-swap":
                    CMD.sh(f"mkswap -L {label} {device}")


FS = FsService()
