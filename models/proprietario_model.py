from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text,Date
from sqlalchemy.orm import relationship
from core.configs import settings
from models.condominio_model import UnidadeModel, IndividuoModel


class ProprietarioModel(settings.DBBaseModel):
    __tablename__ = 'proprietario_unidade'

    id = Column(Integer, primary_key=True, autoincrement=True)  
    
    individuo_id = Column(Integer, ForeignKey('individuo.id'))
    individuo = relationship(
        IndividuoModel,
    )
    
    unidade_id = Column(Integer, ForeignKey('unidade.id'))
    unidade = relationship(
        UnidadeModel,
    )
     
    data_inic = Column(Date)
    data_fim = Column(Date)
    observacao = Column(Text)
    situacao = Column(Boolean, nullable=False, default=True)
   




