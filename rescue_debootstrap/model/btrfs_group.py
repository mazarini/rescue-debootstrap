from pydantic import BaseModel

from rescue_debootstrap.model.btrfs_device import BtrfsDevice
from rescue_debootstrap.model.btrfs_node import BtrfsNode


class BtrfsGroup(BaseModel):
    label: str
    type: str
    devices: list[BtrfsDevice]
    tree: list[BtrfsNode]
