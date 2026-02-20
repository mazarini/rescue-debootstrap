from rescue_debootstrap.util.command import CMD
from rescue_debootstrap.util.config_util import CONFIG


class umount:
    def device(self, mountpoint: str, options: str = "") -> None:
        CMD.sh(f"umount {options} {mountpoint}")

    def all(self) -> None:
        CMD.sh(f"umount -l {CONFIG.host.mountpoint} || true")


UMOUNT = umount()
