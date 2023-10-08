from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class LogSchema(BaseModel):
    id: Optional[int] = None
    table_name:str
    action:str
    error:Optional[str]
    reg_old: Optional[dict]
    reg_new: Optional[dict]
    usuario_id : Optional[int]
    log_date: datetime


    class Config:
        orm_mode = True