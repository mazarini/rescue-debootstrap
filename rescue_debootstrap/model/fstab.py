from pydantic import BaseModel


class Fstab(BaseModel):
    label: str
    type: str
    mountpoint: str
