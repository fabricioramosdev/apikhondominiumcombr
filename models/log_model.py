from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, JSON
from sqlalchemy.orm import relationship

from core.configs import settings


class LogModel(settings.DBBaseModel):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(Text)
    action = Column(Text)
    error =  Column(Text)
    reg_old = Column(JSON)
    reg_new = Column(JSON)
    user_id = Column(Integer, ForeignKey('usuarios.id'))
    log_date =  Column(DateTime)
