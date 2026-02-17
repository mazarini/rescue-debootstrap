from pydantic import BaseModel

from rescue_debootstrap.model.disk_model import DiskModelSpec


class Disk(BaseModel):
    number: int
    device: str

    def print(self, disk_model: DiskModelSpec, partitions: list) -> int:
        print(f"\n    + Disk {self.number}: device={self.device}")
        end = disk_model.start_sector - 1
        for p in partitions:
            end += p.print(disk_model, self)
        return disk_model.end_sector - end
