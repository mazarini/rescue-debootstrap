from rescue_debootstrap.model.partition_registry import REGISTRY
from rescue_debootstrap.service.partition_service import PARTITION
from rescue_debootstrap.service.security_service import SECURITY
from rescue_debootstrap.util.config_util import CONFIG
from rescue_debootstrap.util.env_util import ENV


def main() -> None:
    print("\n\n" + "=" * 80)
    print("Rescue debootstrap installer")
    print("=" * 80)
    ENV.print()
    print(f"\nInstall {CONFIG.host.full_name} on {CONFIG.host.rescue_name}")
    SECURITY.rescue()
    SECURITY.confirmDestructiveAction()
    PARTITION.create_storages(CONFIG.storage_groups)
    print("\nInstallation complete !")
    REGISTRY.print()


if __name__ == "__main__":
    main()
