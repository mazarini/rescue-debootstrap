from rescue_debootstrap.model.partition_registry import REGISTRY
from rescue_debootstrap.util.command import CMD
from rescue_debootstrap.util.config_util import CONFIG


class mount:
    def device(self, device: str, mountpoint: str, options: str = "") -> None:
        CMD.sh(f"mount {options} {device} {mountpoint}")

    def chroot_all(self) -> None:
        CMD.chroot("mount -a")

    def rbind(self) -> None:
        for device in ["/dev", "/proc", "/sys", "/run"]:
            self.device(device, f"{CONFIG.host.mountpoint}{device}", "--rbind")

    def all(self) -> None:
        print(f"Mounting all {len(CONFIG.fstab)} filesystems...")
        for fs in CONFIG.fstab:
            if fs.type != "swap":
                CMD.sh(f"mkdir -p {CONFIG.host.mountpoint}{fs.mountpoint}")
            if fs.type == "btrfs":
                CMD.sh(
                    f"mount -o subvol={fs.label} {REGISTRY.get(fs.label)} {CONFIG.host.mountpoint}{fs.mountpoint}"
                )
            if fs.type == "vfat":
                CMD.sh(
                    f"mount {REGISTRY.get(fs.label)} {CONFIG.host.mountpoint}{fs.mountpoint}"
                )
            if fs.type == "ext4":
                CMD.sh(
                    f"mount {REGISTRY.get(fs.label)} {CONFIG.host.mountpoint}{fs.mountpoint}"
                )


MOUNT = mount()
