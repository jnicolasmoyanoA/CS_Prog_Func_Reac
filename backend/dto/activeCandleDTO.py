from pydantic import BaseModel
from datetime import datetime

class ActiveCandleStreamDTO(BaseModel):
    token: str
    open_time: datetime
    updated_at: int 
    open: float
    high: float
    low: float
    close: float
    volume: float

    class Config:
        orm_mode = True
