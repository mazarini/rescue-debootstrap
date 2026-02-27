from pathlib import Path

from rescue_debootstrap.model.debootstrap import Debootstrap
from rescue_debootstrap.util.command import CMD
from rescue_debootstrap.util.config_util import CONFIG
from rescue_debootstrap.util.file_util import FILE
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
        MOUNT.bind()
        CMD.chroot("chattr +m /boot")
        self._create_hostname()
        self._create_hosts()

    def _create_hostname(self):
        hostname = f"{CONFIG.host.hostname}.{CONFIG.host.domain}"
        FILE.create(Path("/etc/hostname"), hostname)

    def _create_hosts(self):
        hosts_content = f"""# Configuration IPv4
127.0.0.1   localhost localhost@localdomain
127.0.1.1   {CONFIG.host.hostname} {CONFIG.host.hostname}.{CONFIG.host.domain}

# Configuration IPv6
::1         localhost ip6-localhost ip6-loopback
ff02::1     ip6-allnodes
ff02::2     ip6-allrouters
"""
        FILE.create(Path("/etc/hosts"), hosts_content)


DEBOOTSTRAP = DebootstrapService()
