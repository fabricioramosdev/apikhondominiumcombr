from typing import Optional
from pydantic import BaseModel
from datetime import datetime



class VisitanteSchema(BaseModel):
    id: Optional[int] = None
    individuo_id: int
    unidade_id: int
    data_inic: Optional[datetime] = datetime.now()
    data_fim: Optional[datetime] 
    tipo_visita: Optional[str] = 'social'
    observacao: Optional[str]
    situacao : Optional[bool] = True

    class Config:
        orm_mode = True

