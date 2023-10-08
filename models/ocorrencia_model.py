from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text,Date, DateTime
from sqlalchemy.orm import relationship
from core.configs import settings
from models.condominio_model import UnidadeModel, IndividuoModel


class OcorrenciaModel(settings.DBBaseModel):
    __tablename__ = 'ocorrencia'

    id = Column(Integer, primary_key=True, autoincrement=True)  
      
    
    unidade_id = Column(Integer, ForeignKey('unidade.id') )
    unidade = relationship(
        UnidadeModel,
    )
    
    tipo_ocorrencia =  Column(String)
    notificar_ocorrencia = Column(String)
     
    data_fato = Column(DateTime)

    dsc_fato = Column(Text)    
    dsc_conclusao = Column(Text)
    
    situacao = Column(Boolean, nullable=False, default=True)
   




