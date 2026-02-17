from pydantic import BaseModel, Field

from rescue_debootstrap.model.host import Host
from rescue_debootstrap.model.storage_group import StorageGroup


class InstallConfig(BaseModel):
    host: Host
    storage_groups: list[StorageGroup] = Field(default_factory=list)
