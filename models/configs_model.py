from sqlalchemy import Column, Integer, String,  Boolean, Text
from core.configs import settings


class ConfigsNotificarOcorrenciateModel(settings.DBBaseModel):
    """
    Represents a table named `configs_notificar_ocorrencia` in the database.

    Fields:
    - `id`: An auto-incrementing integer column that serves as the primary key for the table.
    - `valor`: A string column that stores a value.
    - `observacao`: A text column that stores an observation.
    - `situacao`: A boolean column that stores a situation.
    """

    __tablename__ = 'configs_notificar_ocorrencia'
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(String(length=255))
    observacao = Column(Text)
    situacao = Column(Boolean, nullable=False, default=True)


class ConfigsTipoOcorrenciateModel(settings.DBBaseModel):
    """
    Represents a table named 'configs_tipo_ocorrencia' in the database.

    Fields:
    - id: An auto-incrementing integer column that serves as the primary key.
    - valor: A string column.
    - observacao: A text column.
    - situacao: A boolean column.
    """

    __tablename__ = 'configs_tipo_ocorrencia'

    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(String)
    observacao = Column(Text)
    situacao = Column(Boolean, nullable=False, default=True)



class ConfigsTipoVisitanteModel(settings.DBBaseModel):
    """
    Represents a table named 'configs_tipo_visitante' in the database.
    Inherits from the `DBBaseModel` class defined in the `settings` module.
    """

    __tablename__ = 'configs_tipo_visitante'

    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(String(length=255))
    observacao = Column(Text)
    situacao = Column(Boolean, nullable=False, default=True)


class ConfigsUfModel(settings.DBBaseModel):
    __tablename__ = 'configs_uf'
    id = Column(Integer, primary_key=True, autoincrement=True)  
    valor =  Column(String(length=255))
    observacao = Column(Text)
    situacao = Column(Boolean, nullable=False, default=True)

     