from pydantic import BaseModel


class BtrfsNode(BaseModel):
    label: str
    type: str
    name: str
