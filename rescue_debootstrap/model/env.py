from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Env:
    app_env: str
    app_debug: bool
    dry_run: bool
    host: str
    project_dir_path: Path

    def getAppEnv(self) -> str:
        return self.app_env

    def isDebug(self) -> bool:
        return self.app_debug

    def isDryRun(self) -> bool:
        return self.dry_run

    def getHost(self) -> str:
        return self.host

    def getProjectDirPath(self) -> Path:
        return self.project_dir_path

    def getConfigDirPath(self) -> Path:
        return Path(self.getProjectDirPath()) / "config"

    def getHostConfigDirPath(self) -> Path:
        return Path(self.getConfigDirPath()) / self.host
