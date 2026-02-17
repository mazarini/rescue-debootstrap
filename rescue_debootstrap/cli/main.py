from rescue_debootstrap.util.config_util import CONFIG
from rescue_debootstrap.util.env_util import ENV


def main() -> None:
    ENV.print()
    print(f"\nInstall {CONFIG.host.full_name} on {CONFIG.host.rescue_name}")
    for sg in CONFIG.storage_groups:
        sg.print()
    print(f"\nHost {CONFIG.host.full_name} is ready")


if __name__ == "__main__":
    main()
