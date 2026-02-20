from rescue_debootstrap.model.partition_registry import REGISTRY
from rescue_debootstrap.service.fs_service import FS
from rescue_debootstrap.service.partition_service import PARTITION
from rescue_debootstrap.service.security_service import SECURITY
from rescue_debootstrap.util.btrfs import BTRFS
from rescue_debootstrap.util.config_util import CONFIG
from rescue_debootstrap.util.env_util import ENV
from rescue_debootstrap.util.mount import MOUNT
from rescue_debootstrap.util.umount import UMOUNT


def main() -> None:
    print("\n\n" + "=" * 80)
    print("Rescue debootstrap installer")
    print("=" * 80)
    ENV.print()
    print(f"\nInstall {CONFIG.host.full_name} on {CONFIG.host.rescue_name}")
    SECURITY.rescue()
    SECURITY.confirmDestructiveAction()

    UMOUNT.all()
    PARTITION.create_storages(CONFIG.storage_groups)
    FS.create_fs(CONFIG.storage_groups)
    BTRFS.create_btrfs_groups(CONFIG.btrfs_groups)
    MOUNT.all()

    print("\nInstallation complete !")
    REGISTRY.print()


if __name__ == "__main__":
    main()
