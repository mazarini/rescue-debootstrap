from pydantic import BaseModel

from rescue_debootstrap.model.host import Host


class InstallConfig(BaseModel):
    host: Host


#    storages: list[StorageGroup] = Field(default_factory=list)
#    disk_model: dict[str, DiskModelSpec] = Field(default_factory=dict)
