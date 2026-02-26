# command.py
import shlex
import subprocess

from rescue_debootstrap.exception.command_exception import CommandException
from rescue_debootstrap.util.config_util import CONFIG
from rescue_debootstrap.util.env_util import ENV


class Command:
    def sh(self, command: str) -> None:
        """Exécute une commande bash et affiche toute la sortie en temps réel.
        Lève CommandError si la commande échoue.
        """
        print(f"+ {command}", flush=True)
        if ENV.dry_run:
            print("Dry-run mode: Command not executed.", flush=True)
            return

        # subprocess en mode ligne par ligne pour éviter le buffering
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # line-buffered
        )

        for line in process.stdout:
            print(line, end="", flush=True)  # flush immédiat

        process.wait()
        if process.returncode != 0:
            raise CommandException(command, process.returncode)

    def chroot(self, command: str) -> None:
        """Exécute une commande dans le chroot et affiche toute la sortie."""
        # sécurise la commande pour éviter les problèmes de quotes
        safe_cmd = shlex.quote(command)
        self.sh(f"chroot {CONFIG.host.mountpoint} /bin/bash -c {safe_cmd}")


# instance globale
CMD = Command()
