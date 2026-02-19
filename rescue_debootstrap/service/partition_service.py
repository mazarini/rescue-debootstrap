from rescue_debootstrap.model.disk import Disk
from rescue_debootstrap.model.disk_model import DiskModelSpec
from rescue_debootstrap.model.partition import Partition
from rescue_debootstrap.model.partition_registry import REGISTRY
from rescue_debootstrap.model.storage_group import StorageGroup
from rescue_debootstrap.util.parted import PARTED
from rescue_debootstrap.util.sgdisk import SGDISK


class PartionService:
    def create_storages(self, storages: list[StorageGroup]):
        for storage in storages:
            self.create_storage(storage)

    def create_storage(self, storage: StorageGroup):
        for disk in storage.disks:
            self.create_disk(storage.disk_model, disk, storage.partitions)
        for partition in storage.partitions:
            for disk in storage.disks:
                if len(storage.disks) > 1:
                    label = f"{partition.label}-{disk.number}"
                else:
                    label = partition.label
                PARTED.name(disk.device, partition.number, label)
                REGISTRY.add(label, partition.device(storage.disk_model, disk))

    def create_disk(
        self, disk_model: DiskModelSpec, disk: Disk, partitions: list[Partition]
    ):
        self.raz_disk(disk)
        start = disk_model.start_sector
        for partition in partitions:
            type = "fat32" if partition.type == "efi" else partition.type
            PARTED.mkpart(
                device=disk.device,
                type=type,
                start=start,
                end=start + partition.size - 1,
                unit="s",
            )
            if partition.type == "efi":
                PARTED.set_esp(device=disk.device, number=partition.number)
            start += partition.size

    def raz_disk(self, disk: Disk):
        SGDISK.zap_all(disk.device)
        PARTED.mklabel(disk.device)


PARTITION = PartionService()
