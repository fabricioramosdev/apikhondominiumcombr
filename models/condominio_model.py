from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, UniqueConstraint, Date
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from core.configs import settings


class CondominioModel(settings.DBBaseModel):
    __tablename__ = 'condominio'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String(25))
    razao_social = Column(String(255))
    nome_fantasia = Column(String(255))
    telefone = Column(String(15))
    email = Column(String(255))
    endereco = Column(String(255))
    complemento = Column(String(100))
    bairro = Column(String(100))
    cidade = Column(String(100))
    uf = Column(String(15))
    situacao = Column(Boolean, nullable=False, default=True)
   
    def __repr__(self) -> str:
        inst = {'id':self.id, 
              'cnpj':self.cnpj, 'razao_social':self.razao_social, 
              'nome_fantasia':self.nome_fantasia, 'telefone':self.telefone,
              'email':self.email, 'endereco':self.endereco,'complemento':self.complemento, 
              'bairro':self.bairro,'cidade':self.cidade,'uf':self.uf}
        return  str(inst)
    
 
 
class PredioModel(settings.DBBaseModel):
    __tablename__ = 'predio'

    id = Column(Integer, primary_key=True, autoincrement=True)  
    uuid = Column(String(15))

    condominio_id = Column(Integer, ForeignKey('condominio.id'))
    condominio = relationship(
        "CondominioModel",
    )
     
    observacao = Column(Text)
    situacao = Column(Boolean, nullable=False, default=True)
   

class UnidadeModel(settings.DBBaseModel):
    __tablename__ = 'unidade'
    id = Column(Integer, primary_key=True, autoincrement=True)  
    uuid = Column(String(15))
    predio_id = Column(Integer, ForeignKey('predio.id'))
    predio = relationship(
        "PredioModel",
    )
    observacao = Column(Text)
    situacao = Column(Boolean, nullable=False,  default=True)
   


class IndividuoModel(settings.DBBaseModel):
    __tablename__ = 'individuo'
    id = Column(Integer, primary_key=True, autoincrement=True)  
    nome = Column(String(255))
    cpf = Column(String(15))
    rg = Column(String(15))
    data_nasc =  Column(Date)
    genero = Column(String(15)) # configs
    telefone = Column(String(15))
    celular = Column(String(15))
    email = Column(String(255))
    cep = Column(String(15))
    endereco = Column(Text)
    complemento = Column(String(255))
    bairro = Column(String(15))
    cidade = Column(String(255))
    estado = Column(String(15))
    observacao = Column(Text)
    situacao = Column(Boolean, nullable=False, default=True)
    condominio_id = Column(Integer, ForeignKey('condominio.id'))
    condominio = relationship(
        "CondominioModel",
    )
    
    __table_args__ = (
        UniqueConstraint('cpf', 'condominio_id', name='uq_cpf_condominio'),
    )
    

   