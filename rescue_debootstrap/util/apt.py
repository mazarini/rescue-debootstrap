from pathlib import Path

from rescue_debootstrap.util.command import CMD
from rescue_debootstrap.util.config_util import CONFIG
from rescue_debootstrap.util.file_util import FILE


class AptUtil:
    def __init__(self):
        # /etc/apt/source.list to be create
        self._initialized = False

    def _initialize(self) -> None:
        if self._initialized:
            # stop if previously created
            return
        # Don't create again
        self._initialized = True
        # Create source.file
        target = Path("/etc/apt/sources.list")
        content = self._source_file()
        FILE.create(target, content)
        # First and unique update + dist-upgrade
        CMD.chroot("apt-get update", CONFIG.host.mountpoint)
        CMD.chroot("apt-get -y dist-upgrade", CONFIG.host.mountpoint)

    # ─────────────────────────────────────────────

    def _run(self, args: str) -> None:
        self._initialize()  # if needed
        CMD.chroot(f"apt-get -y {args}", CONFIG.host.mountpoint)

    # ─────────────────────────────────────────────

    def update(self) -> None:
        self._initialize()  # update + upgrade

    def upgrade(self) -> None:
        self._initialize()  # update + upgrade

    def dist_upgrade(self) -> None:
        self.upgrade()

    def install(self, package: str) -> None:
        self._run(f"install {package}")

    def purge(self, package: str) -> None:
        self._run(f"purge {package}")

    def autoremove(self) -> None:
        self._run("--purge autoremove")

    # ─────────────────────────────────────────────

    def _source_file(self) -> str:
        mirror = CONFIG.debootstrap.mirror
        suite = CONFIG.debootstrap.suite
        components = " ".join(CONFIG.debootstrap.components)
        return f"""\
deb {mirror} {suite} {components}
deb {mirror} {suite}-updates {components}
deb http://security.debian.org/debian-security {suite}-security {components}
"""


APT = AptUtil()
