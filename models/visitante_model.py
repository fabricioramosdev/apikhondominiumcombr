from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from core.configs import settings
from models.condominio_model import UnidadeModel, IndividuoModel


class VisitanteModel(settings.DBBaseModel):
    __tablename__ = 'visitante_unidade'

    id = Column(Integer, primary_key=True, autoincrement=True)

    individuo_id = Column(Integer, ForeignKey('individuo.id'))
    individuo = relationship(
        IndividuoModel,
    )

    unidade_id = Column(Integer, ForeignKey('unidade.id'))
    unidade = relationship(
        UnidadeModel,
    )
    tipo_visita = Column(String)

    data_inic = Column(DateTime)
    data_fim = Column(DateTime)
    observacao = Column(Text)
    situacao = Column(Boolean, nullable=False, default=True)

