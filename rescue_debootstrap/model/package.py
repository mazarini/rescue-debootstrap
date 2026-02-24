from pydantic import BaseModel, Field

from rescue_debootstrap.model.sed_command import SedCommand


class Package(BaseModel):
    name: str | None = None  # peut être absent
    files: list[str] = Field(default_factory=list)  # vide par défaut
    sed: list[SedCommand] = Field(default_factory=list)  # vide par défaut
    cmd: list[str] = Field(default_factory=list)  # vide par défaut
