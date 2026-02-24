from rescue_debootstrap.model.package import Package
from rescue_debootstrap.util.apt import APT
from rescue_debootstrap.util.command import CMD
from rescue_debootstrap.util.config_util import CONFIG
from rescue_debootstrap.util.file_util import FILE


class PackageService:
    def install_all(self):
        for pkg in CONFIG.packages:
            self.install(pkg)

    def install(self, pkg: Package):
        print(f"\n=== Processing package: {pkg.name or 'files-only'} ===", flush=True)

        # 1️⃣ Installation apt
        if pkg.name:
            APT.install(pkg.name)

        # 2️⃣ Fichiers template
        FILE.copy(pkg.files)

        # 3️⃣ Sed (pas de chroot)
        for sed in pkg.sed:
            FILE.apply_sed(sed.file, sed.filter, sed.replace)

        # 4️⃣ Commandes post-install
        for command in pkg.cmd:
            CMD.chroot(command, CONFIG.host.mountpoint)

    # -------------------------------------------------------------

    def reinstall_packages(self):
        for pkg in reversed(CONFIG.packages):
            if pkg.name:
                CMD.chroot(f"apt-get purge -y {pkg.name}", CONFIG.host.mountpoint)
        CMD.chroot("apt-get autoremove -y --purge", CONFIG.host.mountpoint)
        self.install_all()


PACKAGE = PackageService()
