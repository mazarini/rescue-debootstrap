from __future__ import annotations

from pathlib import Path

from dotenv import dotenv_values  # ← la fonction qui lit sans modifier os.environ

from rescue_debootstrap.model.env import Env


class EnvUtil:
    def _str_to_bool(self, value: str | None) -> bool:
        """Conversion robuste str → bool"""
        if value is None:
            return False
        lowered = value.strip().lower()
        return lowered in {"1", "true", "yes", "on", "oui", "y"}

    def _get_project_root_path(self) -> Path:
        return Path(__file__).resolve().parents[2]

    def _get_env_data(self, file: str) -> dict[str, str | None]:
        env_path = self._get_project_root_path() / file
        if not env_path.is_file():
            raise FileNotFoundError(f"Fichier .env introuvable : {env_path}")
        return dotenv_values(env_path, encoding="utf-8")

    def load_env(self) -> Env:
        # Lecture pure → retourne un dict[str, str | None]
        data: dict[str, str | None] = self._get_env_data(".env")
        # Validation des clés obligatoires
        required_keys = {"app_env", "app_debug", "dry_run", "host_config"}
        missing = required_keys - {k for k, v in data.items() if v is not None}
        if missing:
            raise ValueError(f"Clés manquantes dans .env : {', '.join(missing)}")

        return Env(
            app_env=data["app_env"] or "dev",  # fallback if None
            app_debug=self._str_to_bool(data["app_debug"]),
            dry_run=self._str_to_bool(data["dry_run"]),
            host_config=data["host_config"],
            project_dir_path=self._get_project_root_path(),
        )


ENV: Env = EnvUtil().load_env()
