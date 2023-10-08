from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text,Date
from sqlalchemy.orm import relationship
from core.configs import settings
from models.condominio_model import UnidadeModel, IndividuoModel


class PacoteCorrespondeciaModel(settings.DBBaseModel):
    __tablename__ = 'pacote_correspondencia'

    id = Column(Integer, primary_key=True, autoincrement=True)     
     
    unidade_id = Column(Integer, ForeignKey('unidade.id'))
    unidade = relationship(
        UnidadeModel,
    )
    
    destinatario = Column(String(255))
    objeto = Column(Text)
    
    responsavel_recebimento = Column(Integer, ForeignKey('usuarios.id'))
    data_recebimento = Column(Date)
    
    responsavel_retirada = Column(Integer, ForeignKey('usuarios.id'))
    retirado_por = Column(String(255))
    num_doc = Column(String(255))   
    data_retirada = Column(Date)
    
    situacao = Column(Boolean, nullable=False, default=True)
   




