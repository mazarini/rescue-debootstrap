import socket

from rescue_debootstrap.util.config_util import CONFIG


class HostnameMismatchError(Exception):
    pass


class SecurityService:
    def rescue(self) -> None:
        rescue_name = CONFIG.host.rescue_name
        hostname = socket.gethostname()
        if hostname != rescue_name:
            print("\n" + "=" * 40)
            print("Security alert: Are you sure you are on the correct host?")
            print(f"Real hostname:     {hostname}")
            print(f"Espected hostname: {rescue_name}")
            print("See rescue_debootstrap.host.rescue_name in your configuration file.")
            print("=" * 40)
            raise HostnameMismatchError(
                f"Hostname '{hostname}' ne correspond pas à rescue_name '{rescue_name}' !"
            )

    def confirmDestructiveAction(self: str) -> None:
        print("\n" + "=" * 40)
        print("WARNING: This action is destructive and may cause data loss!")
        print("Type 'yes' to confirm and proceed.")
        print("=" * 40)
        confirmation = input("Your choice: ")
        if confirmation.lower() != "yes":
            print("Action cancelled by user.")
            exit(0)


SECURITY = SecurityService()
