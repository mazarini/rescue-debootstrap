from __future__ import annotations

from pathlib import Path

from dotenv import dotenv_values  # ← la fonction qui lit sans modifier os.environ

from rescue_debootstrap.model.env import Env


def _str_to_bool(value: str | None) -> bool:
    """Conversion robuste str → bool"""
    if value is None:
        return False
    lowered = value.strip().lower()
    return lowered in {"1", "true", "yes", "on", "oui", "y"}


def _get_project_root_path() -> Path:
    # Adaptez selon la profondeur réelle (ici 3 niveaux depuis util/env_util.py)
    return Path(__file__).resolve().parents[2]


def _get_env_data(file: str) -> dict[str, str | None]:
    _get_project_root_path() / file
    env_path = Path(file)
    if not env_path.is_file():
        raise FileNotFoundError(f"Fichier .env introuvable : {env_path}")
    return dotenv_values(env_path, encoding="utf-8")


def load_env() -> Env:
    # Lecture pure → retourne un dict[str, str | None]
    data: dict[str, str | None] = _get_env_data(".env")
    # Validation des clés obligatoires
    required_keys = {"app_env", "app_debug", "dry_run", "host"}
    missing = required_keys - {k for k, v in data.items() if v is not None}
    if missing:
        raise ValueError(f"Clés manquantes dans .env : {', '.join(missing)}")

    return Env(
        app_env=data["app_env"] or "development",  # fallback si None
        app_debug=_str_to_bool(data["app_debug"]),
        dry_run=_str_to_bool(data["dry_run"]),
        host=data["host"],
        project_dir_path=_get_project_root_path(),
    )


def print_env() -> None:
    print("Environnement chargé :")
    print(f"  Host    : {ENV.getHost()}")
    print(f"  Debug   : {ENV.isDebug()}")
    print(f"  Dry run : {ENV.isDryRun()}")


ENV: Env = load_env()

if __name__ == "__main__":
    try:
        print_env()
    except Exception as e:
        print(f"Erreur : {type(e).__name__}: {e}")
