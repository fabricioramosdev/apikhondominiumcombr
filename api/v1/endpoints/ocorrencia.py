from datetime import datetime
from typing import List


from enum import Enum

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.ocorrencia_model import OcorrenciaModel
from models.condominio_model import (UnidadeModel,
                                     PredioModel)


from models.usuario_model import UsuarioModel
from models.log_model import LogModel

from schemas.ocorrencia_schema import OcorrenciaSchema

from core.deps import get_session, get_current_user, set_log

router = APIRouter()


# POST Ocorrencias
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=OcorrenciaSchema)
async def post_ocorrencia(ocorrencia: OcorrenciaSchema, user: UsuarioModel = Depends(get_current_user),
                          db: AsyncSession = Depends(get_session)):

    try:
        data: OcorrenciaModel = OcorrenciaModel(
            unidade_id=ocorrencia.unidade_id,
            tipo_ocorrencia=ocorrencia.tipo_ocorrencia,
            notificar_ocorrencia=ocorrencia.notificar_ocorrencia,
            data_fato=ocorrencia.data_fato,
            dsc_fato=ocorrencia.dsc_fato,
            dsc_conclusao=ocorrencia.dsc_conclusao,
            situacao=ocorrencia.situacao,
        )

        db.add(data)
        await db.commit()

        # log registro
        await set_log(LogModel(
            table_name=OcorrenciaModel.__tablename__,
            action='post',
            reg_new=str(ocorrencia.dict()),
            user_id=user.id,
            log_date=datetime.now()
        ), db)

    except exc.IntegrityError:
        raise HTTPException(detail='Dados não encontrados',
                            status_code=status.HTTP_404_NOT_FOUND)

    return data


# GET Ocorrencias
@router.get('/', response_model=List[OcorrenciaSchema])
async def get_ocorrencias(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(OcorrenciaModel)
        result = await session.execute(query)
        ocorrencias: List[OcorrenciaModel] = result.scalars(
        ).unique().all()

        return ocorrencias


# GET Ocorrencia ID

@router.get('/{id}', response_model=OcorrenciaSchema, status_code=status.HTTP_200_OK)
async def get_ocorrencia(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(OcorrenciaModel).filter(OcorrenciaModel.id == id)
        result = await session.execute(query)
        ocorrencia: OcorrenciaModel = result.scalars().unique().one_or_none()

        if ocorrencia:
            return ocorrencia
        else:
            raise HTTPException(detail='Ocorrencia não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)

# GET Ocorrencias Condominio ID

@router.get('/condominio/{id}', response_model=List[OcorrenciaSchema], status_code=status.HTTP_200_OK)
async def get_ocorrencia_condominio(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(OcorrenciaModel).join(
            UnidadeModel, UnidadeModel.id == OcorrenciaModel.unidade_id).join(
                PredioModel, PredioModel.id == UnidadeModel.predio_id
        ).filter(PredioModel.condominio_id == id)
        result = await session.execute(query) 
        ocorrencias: List[OcorrenciaModel] =  result.scalars().unique().all()
        return ocorrencias 


# PUT Ocorrencias
@router.put('/{id}', response_model=OcorrenciaSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_ocorrencia(id: int, ocorrencia: OcorrenciaSchema,  db: AsyncSession = Depends(get_session),
                         user: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(OcorrenciaModel).filter(OcorrenciaModel.id == id)
        result = await session.execute(query)
        ocorrencia_update: OcorrenciaModel = result.scalars().unique().one_or_none()

        # log registro
        await set_log(LogModel(
            table_name=OcorrenciaModel.__tablename__,
            action='put',
            reg_old=str(ocorrencia_update),
            reg_new=str(ocorrencia.dict()),
            user_id=user.id,
            log_date=datetime.now()
        ), db)

        if ocorrencia_update:

            if ocorrencia.unidade_id:
                ocorrencia_update.unidade_id = ocorrencia.unidade_id

            if ocorrencia.tipo_ocorrencia:
                ocorrencia_update.tipo_ocorrencia = ocorrencia.tipo_ocorrencia

            if ocorrencia.notificar_ocorrencia:
                ocorrencia_update.notificar_ocorrencia = ocorrencia.notificar_ocorrencia

            if ocorrencia.data_fato:
                ocorrencia_update.data_fato = ocorrencia.data_fato

            if ocorrencia.dsc_fato:
                ocorrencia_update.dsc_fato = ocorrencia.dsc_fato

            if ocorrencia.dsc_conclusao:
                ocorrencia_update.dsc_conclusao = ocorrencia.dsc_conclusao

            if ocorrencia.situacao:
                ocorrencia_update.situacao = ocorrencia.situacao

            await session.commit()
            return ocorrencia_update
        else:
            raise HTTPException(detail='Ocorrencia não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)

# DELETE Ocorrencias


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_ocorrencia(id: int,  user: UsuarioModel = Depends(get_current_user),
                            db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(OcorrenciaModel).filter(OcorrenciaModel.id == id)
        result = await session.execute(query)
        ocorrencia_delete: OcorrenciaModel = result.scalars().unique().one_or_none()

        if ocorrencia_delete:
            await session.delete(ocorrencia_delete)
            await session.commit()

            # log registro
            await set_log(LogModel(
                table_name=OcorrenciaModel.__tablename__,
                action='delete',
                reg_old=str(ocorrencia_delete),
                user_id=user.id,
                log_date=datetime.now()
            ), db)

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Ocorrencia não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
