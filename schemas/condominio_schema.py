from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date
from enum import Enum

class CondominioSchema(BaseModel):
    id: Optional[int] = None
    cnpj: str
    razao_social: str
    nome_fantasia: Optional[str]
    telefone: Optional[str]
    email: Optional[str]
    endereco: Optional[str]
    complemento: Optional[str]
    bairro: Optional[str]
    cidade: Optional[str]
    uf: Optional[str]

    class Config:
        orm_mode = True


class PredioSchema(BaseModel):
    id: Optional[int] = None
    uuid: str
    condominio_id: int
    observacao: Optional[str] = None

    class Config:
        orm_mode = True


class UnidadeSchema(BaseModel):
    id: Optional[int] = None
    uuid: str
    predio_id: int
    observacao: Optional[str] = None

    class Config:
        orm_mode = True
  

class IndividuoSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    cpf: Optional[str] = None
    rg: Optional[str] = None
    data_nasc: Optional[date] 
    genero: Optional[str] = None
    telefone: Optional[str] = None
    celular: Optional[str] = None
    email: Optional[str] = None
    cep: Optional[str] = None
    endereco: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    observacao: Optional[str] = None
    situacao: Optional[bool] = True
    condominio_id: int


    class Config:
        orm_mode = True

class IndividuoPutSchema(BaseModel):
    id: Optional[int] = None
    nome: Optional[str]
    cpf: Optional[str]
    rg: Optional[str] = None
    data_nasc: Optional[date] 
    genero: Optional[str] = None
    telefone: Optional[str] = None
    celular: Optional[str] = None
    email: Optional[str] = None
    cep: Optional[str] = None
    endereco: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    observacao: Optional[str] = None
    situacao: Optional[bool] = True
    condominio_id: int


    class Config:
        orm_mode = True

