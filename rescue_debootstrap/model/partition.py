from pydantic import BaseModel

from rescue_debootstrap.model.disk import Disk
from rescue_debootstrap.model.disk_model import DiskModelSpec


class Partition(BaseModel):
    number: int
    type: str
    size: int
    label: str

    def device(self, disk_model: DiskModelSpec, disk: Disk) -> str:
        if disk_model.type == "nvme":
            return f"{disk.device}p{self.number}"
        return f"{disk.device}{self.number}"

    def hSize(self, disk_model: DiskModelSpec) -> str:
        size_kb = self.size * disk_model.sector_size / 1024  # sectors to KiB
        if size_kb < 1024:
            return f"{size_kb} KiB"
        size_mb = size_kb / 1024  # KiB to MiB
        if size_mb < 1024:
            return f"{size_mb} MiB"
        size_gb = size_mb / 1024  # MiB to GiB
        return f"{size_gb:.1f} GiB"

    def print(self, disk_model: DiskModelSpec, disk: Disk) -> int:
        device = self.device(disk_model, disk)
        print(
            f"      - Partition {device}: type={self.type}, size={self.hSize(disk_model)}, label={self.label}(-{disk.number})"
        )
        return self.size
