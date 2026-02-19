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


MOUNT = mount()
