from datetime import datetime
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.proprietario_model import ProprietarioModel
from models.condominio_model import (UnidadeModel,
                                     PredioModel)
from models.usuario_model import UsuarioModel
from models.log_model import LogModel

from schemas.proprietario_schema import ProprietarioSchema

from core.deps import get_session, get_current_user, set_log

router = APIRouter()

# POST Proprietario


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProprietarioSchema)
async def post_proprietario(proprietario: ProprietarioSchema, user: UsuarioModel = Depends(get_current_user),
                            db: AsyncSession = Depends(get_session)):

    try:
        data: ProprietarioModel = ProprietarioModel(
            individuo_id=proprietario.individuo_id,
            unidade_id=proprietario.unidade_id,
            data_inic=proprietario.data_inic,
            data_fim=proprietario.data_fim,
            observacao=proprietario.observacao,
            situacao=proprietario.situacao,
        )

        db.add(data)
        await db.commit()

        # log registro
        await set_log(LogModel(
            table_name=ProprietarioModel.__tablename__,
            action='post',
            reg_new=str(proprietario.dict()),
            user_id=user.id,
            log_date=datetime.now()
        ), db)

    except exc.IntegrityError:
        raise HTTPException(detail='Dados não encontrados',
                            status_code=status.HTTP_404_NOT_FOUND)

    return data


# GET Proprietarios
@router.get('/', response_model=List[ProprietarioSchema])
async def get_proprietarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProprietarioModel)
        result = await session.execute(query)
        proprietarios: List[ProprietarioModel] = result.scalars(
        ).unique().all()

        return proprietarios

# GET Proprietario ID


@router.get('/{id}', response_model=ProprietarioSchema, status_code=status.HTTP_200_OK)
async def get_proprietario(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProprietarioModel).filter(ProprietarioModel.id == id)
        result = await session.execute(query)
        proprietario: ProprietarioModel = result.scalars().unique().one_or_none()

        if proprietario:
            return proprietario
        else:
            raise HTTPException(detail='Proprietario não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)


# GET Proprietario Condominio ID
@router.get('/condominio/{id}', response_model=List[ProprietarioSchema], status_code=status.HTTP_200_OK)
async def get_proprietarios_condominio(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProprietarioModel).join(UnidadeModel,
                                               UnidadeModel.id == ProprietarioModel.unidade_id).join(
                                                   PredioModel, PredioModel.id == UnidadeModel.predio_id
        ).filter(PredioModel.condominio_id == id)

        result = await session.execute(query)
        proprietarios: List[ProprietarioModel] = result.scalars().unique().all()

        if proprietarios:
            return proprietarios
        else:
            raise HTTPException(detail='Proprietarios não encontrados',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT Proprietario
@router.put('/{id}', response_model=ProprietarioSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_proprietario(id: int, proprietario: ProprietarioSchema,  db: AsyncSession = Depends(get_session),
                           user: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ProprietarioModel).filter(ProprietarioModel.id == id)
        result = await session.execute(query)
        proprietario_update: ProprietarioModel = result.scalars().unique().one_or_none()

        # log registro
        await set_log(LogModel(
            table_name=ProprietarioModel.__tablename__,
            action='put',
            reg_old=str(proprietario_update),
            reg_new=str(proprietario.dict()),
            user_id=user.id,
            log_date=datetime.now()
        ), db)

        if proprietario_update:

            if proprietario.individuo_id:
                proprietario_update.individuo_id = proprietario.individuo_id

            if proprietario.unidade_id:
                proprietario_update.unidade_id = proprietario.unidade_id

            if proprietario.data_inic:
                proprietario_update.data_inic = proprietario.data_inic

            if proprietario.data_fim:
                proprietario_update.data_fim = proprietario.data_fim

            if proprietario.observacao:
                proprietario_update.observacao = proprietario.observacao

            if proprietario.situacao:
                proprietario_update.situacao = proprietario.situacao

            await session.commit()
            return proprietario_update
        else:
            raise HTTPException(detail='Proprietario não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)

# DELETE Proprietario


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_proprietario(id: int,  user: UsuarioModel = Depends(get_current_user),
                              db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(ProprietarioModel).filter(ProprietarioModel.id == id)
        result = await session.execute(query)
        proprietario_delete: ProprietarioModel = result.scalars().unique().one_or_none()

        if proprietario_delete:
            await session.delete(proprietario_delete)
            await session.commit()

            # log registro
            await set_log(LogModel(
                table_name=ProprietarioModel.__tablename__,
                action='delete',
                reg_old=str(proprietario_delete),
                user_id=user.id,
                log_date=datetime.now()
            ), db)

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Proprietario não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
