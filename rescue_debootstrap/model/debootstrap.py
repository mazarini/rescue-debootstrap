from pydantic import BaseModel


class Debootstrap(BaseModel):
    suite: str
    arch: str
    mirror: str
    components: list[str]
    variant: str
    include: list[str]
