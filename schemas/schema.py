from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class RollBase(BaseModel):
    weight: float
    lenght: float


class RollAdd(RollBase):
    
    class Config:
        orm_mode = True


class Roll(RollBase):
    id: int
    added_at: datetime
    deleted_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class StorageBase(BaseModel):
    roll_id: int

class Storage(StorageBase):
    id: int
    
    class Config:
        orm_mode = True        
