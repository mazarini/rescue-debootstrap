from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Env:
    # __init__  arg (required)
    app_env: str
    app_debug: bool
    dry_run: bool
    host_config: str
    project_dir_path: Path
    # __post_init__  arg (computed  after __init__)
    config_dir_path: Path = field(init=False, repr=True)
    host_config_dir_path: Path = field(init=False, repr=True)

    def __post_init__(self) -> None:
        # Calcul + assignation (possible car on utilise object.__setattr__ avec frozen)
        object.__setattr__(self, "config_dir_path", self.project_dir_path / "config")
        object.__setattr__(
            self, "host_config_dir_path", self.config_dir_path / self.host_config
        )

        # Vérifications d'existence (fail-fast)
        if not self.project_dir_path.is_dir():
            self.print()
            raise FileNotFoundError(
                f"Répertoire projet introuvable : {self.project_dir_path}"
            )

        if not self.config_dir_path.is_dir():
            self.print()
            raise FileNotFoundError(
                f"Répertoire config introuvable : {self.config_dir_path}"
            )

        if not self.host_config_dir_path.is_dir():
            self.print()
            raise FileNotFoundError(
                f"Répertoire de configuration host introuvable : {self.host_config_dir_path}"
            )

    def print(self) -> None:
        print("Loaded environment :")
        print(f" - Host config : {self.host_config}")
        print(f" - Debug       : {self.app_debug}")
        print(f" - Dry run     : {self.dry_run}")
        if self.app_debug:
            print(f" - Project dir  : {self.project_dir_path}")
            print(f" - Config dir   : {self.config_dir_path}")
            print(f" - Host config dir : {self.host_config_dir_path}")
