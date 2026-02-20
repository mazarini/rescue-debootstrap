from pydantic import BaseModel


class BtrfsDevice(BaseModel):
    label: str
