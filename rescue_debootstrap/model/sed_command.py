from pydantic import BaseModel


class SedCommand(BaseModel):
    file: str
    filter: str
    replace: str
