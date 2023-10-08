from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date



class DomiciliadoSchema(BaseModel):
    id: Optional[int] = None
    individuo_id: int
    unidade_id: int
    data_inic: Optional[date] = datetime.now()
    data_fim: Optional[date] 
    proprietario: Optional[bool] = False
    observacao: Optional[str]
    situacao : Optional[bool] = True

    class Config:
        orm_mode = True

