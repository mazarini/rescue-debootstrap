import subprocess

from rescue_debootstrap.util.config_util import CONFIG
from rescue_debootstrap.util.env_util import ENV


class command:
    def sh(self, command: str) -> None:
        """Exécute une commande bash et affiche la sortie en temps réel. Retourne le code de retour."""
        print(f"+ {command}")
        if ENV.dry_run:
            print("Dry-run mode: Command not executed.")
            return
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        for line in process.stdout:
            print(line, end="")  # Affiche chaque ligne dès qu'elle arrive
        process.wait()
        if process.returncode != 0:
            print(f"Command failed with return code {process.returncode}")
            exit(process.returncode)

    def chroot(self, command: str) -> None:
        """Exécute une commande dans le chroot de la nouvelle installation."""
        self.sh(f"chroot {CONFIG.host.mountpoint} /bin/bash -c '{command}'")


CMD = command()
