from datetime import datetime
from typing import List

# Docs
# https://github.com/Sidon/py-ufbr
from pyUFbr.baseuf import ufbr 

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from models.condominio_model import  PredioModel, UnidadeModel

from models.configs_model import ConfigsTipoVisitanteModel, ConfigsTipoOcorrenciateModel


from schemas.display_value_schema import DiplayValueSchema

from core.deps import get_session, get_current_user, set_log

router = APIRouter()


@router.get("/DisplayValue/visitantes/tipo_visita/",response_model=List[DiplayValueSchema], status_code=status.HTTP_200_OK)
async def get_tipos_visitantes_display_value(db: AsyncSession = Depends(get_session)):
    async with db as session:
        
        query = select(ConfigsTipoVisitanteModel.id.label('display'), ConfigsTipoVisitanteModel.valor.label('value')).filter(ConfigsTipoVisitanteModel.situacao == True)
        result = await session.execute(query)             
        return [DiplayValueSchema(display=x[0], value=x[1]) for x in result]



@router.get("/DisplayValue/ocorrencias/tipo_ocorrencia/",response_model=List[DiplayValueSchema], status_code=status.HTTP_200_OK)
async def get_tipos_visitantes_display_value(db: AsyncSession = Depends(get_session)):
    async with db as session:
        
        query = select(ConfigsTipoOcorrenciateModel.id.label('display'), ConfigsTipoOcorrenciateModel.valor.label('value')).filter(ConfigsTipoOcorrenciateModel.situacao == True)
        result = await session.execute(query)             
        return [DiplayValueSchema(display=x[0], value=x[1]) for x in result]



@router.get("/DisplayValue/unidades/condominio/{id}",response_model=List[DiplayValueSchema], status_code=status.HTTP_200_OK)
async def get_unidade_display_value_condominio(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        
        query =  select(
             (PredioModel.uuid + ' - ' + UnidadeModel.uuid).label('display'), UnidadeModel.id.label('value')
           
        ).join(PredioModel, PredioModel.id == UnidadeModel.predio_id).order_by(UnidadeModel.uuid)
          
        result = await session.execute(query)
        return [DiplayValueSchema(display=x[0], value=x[1]) for x in result]


@router.get("/DisplayValue/predios/condominio/{id}",response_model=List[DiplayValueSchema], status_code=status.HTTP_200_OK)
async def get_predio_display_value_condominio(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        
        query =  select(
             (PredioModel.uuid).label('display'), PredioModel.id.label('value')
        ).filter(PredioModel.condominio_id==id).order_by(PredioModel.uuid)
          
        result = await session.execute(query)
             
        return [DiplayValueSchema(display=x[0], value=x[1]) for x in result]




@router.get("/DisplayValue/uf",response_model=List[DiplayValueSchema], status_code=status.HTTP_200_OK)
async def get_uf_display_value():
    #print(ufbr.dict_uf)
    return [DiplayValueSchema(display=x, value=x) for x in ufbr.list_uf]


@router.get("/DisplayValue/cidades/uf/{uf}",response_model=List[DiplayValueSchema], status_code=status.HTTP_200_OK)
async def get_cidades_display_value_uf(uf:str):      
    return [DiplayValueSchema(display=x, value=x) for x in ufbr.list_cidades(uf)]