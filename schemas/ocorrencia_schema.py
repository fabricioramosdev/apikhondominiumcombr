from typing import Optional
from pydantic import BaseModel
from datetime import datetime



class OcorrenciaSchema(BaseModel):
    id: Optional[int] = None

    unidade_id: int
    tipo_ocorrencia: Optional[str] = 'notificação'
    notificar_ocorrencia: Optional[str] = 'não notificar'
    
    data_fato: Optional[datetime] = datetime.now()

    dsc_fato: Optional[str]    
    dsc_conclusao: Optional[str]
    
    situacao : Optional[bool] = True

    class Config:
        orm_mode = True

