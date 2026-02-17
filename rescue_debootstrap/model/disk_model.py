from pydantic import BaseModel


class DiskModelSpec(BaseModel):
    type: str
    sector_size: int
    start_sector: int
    end_sector: int
