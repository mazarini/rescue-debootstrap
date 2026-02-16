# rescue_debootstrap/config/loader.py
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from rescue_debootstrap.model.install_config import InstallConfig
from rescue_debootstrap.util.env_util import ENV

# ─── Modèles Pydantic ────────────────────────────────────────────────────────


class Disk:
    device: str
    disk_model: str


class Partition:
    number: int
    type: str
    size: int
    label: str


class StorageGroup:
    disks: list[Disk]
    partitions: list[Partition]


class DiskModelSpec:
    type: str
    sector_size: int
    start_sector: int
    end_sector: int


# ─── Fonctions de chargement ─────────────────────────────────────────────────


def read_single_yaml(path: Path) -> dict[str, Any]:
    """Lit un seul fichier YAML et retourne la racine mazarini_rescue_debootstrap"""
    if not path.is_file():
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data.get("mazarini_rescue_debootstrap", {})
    except Exception as e:
        print(f"Erreur lecture {path.name} : {e}")
        return {}


def merge_all_yaml_in_dir(config_dir: Path, pattern: str = "*.yaml") -> dict[str, Any]:
    """Fusionne TOUS les fichiers YAML du dossier (dernier gagne)"""
    merged: dict[str, Any] = {}

    for file_path in sorted(config_dir.glob(pattern)):
        section = read_single_yaml(file_path)
        if not section:
            continue

        for top_key, value in section.items():
            if top_key in merged:
                if isinstance(merged[top_key], dict) and isinstance(value, dict):
                    merged[top_key].update(value)
                elif isinstance(merged[top_key], list) and isinstance(value, list):
                    merged[top_key].extend(value)
                else:
                    # conflit scalaire → dernier gagne
                    merged[top_key] = value
            else:
                merged[top_key] = value
        if ENV.isDebug():
            print(f"[debug] {file_path.name} loaded")

    return merged


def load_full_config() -> InstallConfig:
    """Charge tout et valide avec Pydantic"""
    # Utilise ENV si tu as déjà cette variable globale
    # Sinon adapte avec Path(__file__).resolve().parents[...]

    config_dir = Path(ENV.getHostConfigDirPath())

    raw_merged = merge_all_yaml_in_dir(config_dir)

    if not raw_merged:
        raise ValueError("Aucune configuration valide trouvée")

    try:
        return InstallConfig.model_validate(raw_merged)
    except ValidationError as e:
        raise ValueError(f"Validation échouée :\n{e}") from e


# ─── Instance globale (chargée une seule fois) ───────────────────────────────

CONFIG: InstallConfig = load_full_config()
