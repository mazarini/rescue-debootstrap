from pathlib import Path

from rescue_debootstrap.model.partition_registry import REGISTRY
from rescue_debootstrap.util.config_util import CONFIG
from rescue_debootstrap.util.file_util import FILE


class FstabService:
    HEADER = "# <file system>\t\t<mount point>\t<type>\t<options>\t<dump>\t<pass>\n"

    def _content(self) -> list[str]:
        lines = [self.HEADER.strip()]

        for device in CONFIG.fstab:
            line = self._line(
                label=device.label,
                fs_type=device.type,
                mountpoint=device.mountpoint,
            )
            lines.append(line)

        return lines

    def _line(self, label: str, fs_type: str, mountpoint) -> str:
        if fs_type == "memory":
            return f"tmpfs {mountpoint} tmpfs defaults,noatime,mode=1777,size=4G 0 0"
        device = REGISTRY.get(label)
        if fs_type == "efi":
            return f"{device} {mountpoint} vfat umask=0077 0 1"
        if fs_type == "ext4":
            return f"{device} {mountpoint} ext4 defaults,noatime 0 1"
        if fs_type == "btrfs":
            return f"{device} {mountpoint} btrfs defaults,{label} 0 1"
        if fs_type == "swap":
            return f"{device} none swap sw 0 0"
        return f"# unknow fs type {label}  {fs_type} {mountpoint}"

    def create_fstab(self):
        content = "\n".join(self._content()) + "\n"
        FILE.create(Path("/etc/fstab"), content)


FSTAB = FstabService()
