import shutil
from pathlib import Path

from rescue_debootstrap.util.command import CMD
from rescue_debootstrap.util.config_util import CONFIG
from rescue_debootstrap.util.env_util import ENV


class FileUtil:
    # ─────────────────────────────────────────────

    def set(self, file: Path):
        """
        Copie un fichier depuis le template vers la cible.
        Priorité :
        1. <suite>/<relative_path>
        2. debian/<relative_path>
        """
        source = self._template_path(file)
        target = self._chroot_path(file)

        self._save(target)

        if not ENV.is_dry_run(f"Copy {source} -> {target}"):
            shutil.copyfile(source, target)

    # ─────────────────────────────────────────────

    def copy(self, files):
        print(f"Copying {len(files)} files...", flush=True)
        for file in files:
            self.set(Path(file))

    # ─────────────────────────────────────────────

    def create(self, file: Path, content: str):
        target = self._chroot_path(file)
        self._save(target)

        if ENV.is_dry_run(f"Write content to {target}"):
            return

        with target.open("w", encoding="utf-8") as f:
            f.write(content)

    # ─────────────────────────────────────────────

    def apply_sed(self, file_path: str, pattern: str, replace: str):

        target = self._chroot_path(Path(file_path))

        if not target.exists():
            raise FileNotFoundError(f"File not found for sed: {target}")

        # backup sécurité
        FILE._save(target)

        sed_cmd = f"sed -i 's|{pattern}|{replace}|' {target}"
        CMD.sh(sed_cmd)

    # ─────────────────────────────────────────────

    def _template_path(self, file: Path) -> Path:
        rel = file.relative_to(file.anchor)

        candidates = [
            ENV.project_dir_path / "template" / CONFIG.debootstrap.suite / rel,
            ENV.project_dir_path / "template" / CONFIG.debootstrap.suite / file.name,
            ENV.project_dir_path / "template" / "debian" / rel,
            ENV.project_dir_path / "template" / "debian" / file.name,
        ]

        for path in candidates:
            if path.exists():
                return path
            print(f"{path} / {file}")

        raise FileNotFoundError(f"Template introuvable pour {file}")

    # ─────────────────────────────────────────────

    def _chroot_path(self, file: Path) -> Path:
        return CONFIG.host.mountpoint / file.relative_to(file.anchor)

    # ─────────────────────────────────────────────

    def _save(self, file: Path):
        """
        Sauvegarde le fichier original une seule fois.
        """
        self._touch(file)

        backup = file.with_name(file.name + ".original")

        if backup.exists():
            return

        if ENV.is_dry_run(f"Backup {file} -> {backup}"):
            return

        shutil.copyfile(file, backup)

    # ─────────────────────────────────────────────

    def _touch(self, file: Path):
        if file.exists():
            return

        if ENV.is_dry_run(f"Create empty {file}"):
            return

        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch(exist_ok=False)


FILE = FileUtil()
