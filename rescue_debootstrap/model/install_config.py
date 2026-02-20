from pydantic import BaseModel, Field

from rescue_debootstrap.model.btrfs_group import BtrfsGroup
from rescue_debootstrap.model.host import Host
from rescue_debootstrap.model.storage_group import StorageGroup


class InstallConfig(BaseModel):
    host: Host
    storage_groups: list[StorageGroup] = Field(default_factory=list)
    btrfs_groups: list[BtrfsGroup] = Field(default_factory=list)
