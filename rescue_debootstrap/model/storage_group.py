from pydantic import BaseModel

from rescue_debootstrap.model.disk import Disk
from rescue_debootstrap.model.disk_model import DiskModelSpec
from rescue_debootstrap.model.partition import Partition


class StorageGroup(BaseModel):
    disk_model: DiskModelSpec
    disks: list[Disk]
    partitions: list[Partition]

    def print(self):
        print(
            f"\n  * Storage Group: disk_model={self.disk_model.type}, sector_size={self.disk_model.sector_size} bytes, start_sector={self.disk_model.start_sector}, end_sector={self.disk_model.end_sector}"
        )
        for disk in self.disks:
            delta = disk.print(self.disk_model, self.partitions)
        if delta > 0:
            print(f"==> Unused space: {delta} sectors")
        if delta == 0:
            print("==> Perfectly used space")
        if delta < 0:
            print(f"==> exceeded space: {-delta} sectors")
