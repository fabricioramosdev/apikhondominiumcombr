
from pydantic import BaseModel

class DiplayValueSchema(BaseModel):
    display:str
    value:str
    class Config:
        orm_mode = True
