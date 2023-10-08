from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date



class PacoteCorrespondeciaSchema(BaseModel):
    id: Optional[int] = None

    unidade_id: int
    destinatario:  Optional[str]
    objeto: Optional[str]
    
    responsavel_recebimento: Optional[int]
    data_recebimento: date = date.today()
    
    responsavel_retirada: Optional[int]
    retirado_por:Optional[str]
    num_doc:Optional[str]
    data_retirada:Optional[date]

    
    situacao : Optional[bool] = True

    class Config:
        orm_mode = True

