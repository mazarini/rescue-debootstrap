from rescue_debootstrap.model.debootstrap import Debootstrap
from rescue_debootstrap.util.command import CMD
from rescue_debootstrap.util.config_util import CONFIG
from rescue_debootstrap.util.mount import MOUNT


class DebootstrapService:
    def run(self, debootstrap: Debootstrap) -> None:
        MOUNT.all()
        print("Running debootstrap...")
        cmd = f"debootstrap --arch={debootstrap.arch}"
        cmd += f" --variant={debootstrap.variant}"
        cmd += f" --include={','.join(debootstrap.include)}"
        cmd += f" --components={','.join(debootstrap.components)}"
        cmd += f" {debootstrap.suite} {CONFIG.host.mountpoint} {debootstrap.mirror}"
        CMD.sh(cmd)
        MOUNT.rbind()


DEBOOTSTRAP = DebootstrapService()
