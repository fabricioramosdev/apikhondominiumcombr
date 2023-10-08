from datetime import datetime
from typing import List


from enum import Enum

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.visitante_model import VisitanteModel
from models.usuario_model import UsuarioModel
from models.log_model import LogModel

from schemas.visitante_schema import VisitanteSchema
from schemas.display_value_schema import DiplayValueSchema

from core.deps import get_session, get_current_user, set_log

router = APIRouter()


    

# POST Visitante
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=VisitanteSchema)
async def post_visitante(visitante: VisitanteSchema, user: UsuarioModel = Depends(get_current_user),
                            db: AsyncSession = Depends(get_session)):

    try:
        data: VisitanteModel = VisitanteModel(
            individuo_id=visitante.individuo_id,
            unidade_id=visitante.unidade_id,
            data_inic=visitante.data_inic,
            data_fim=visitante.data_fim,
            tipo_visita=visitante.tipo_visita,
            observacao=visitante.observacao,
            situacao=visitante.situacao,
        )

        db.add(data)
        await db.commit()

        # log registro
        await set_log(LogModel(
            table_name=VisitanteModel.__tablename__,
            action='post',
            reg_new=str(visitante.dict()),
            user_id=user.id,
            log_date=datetime.now()
        ), db)

    except exc.IntegrityError:
        raise HTTPException(detail='Dados não encontrados',
                            status_code=status.HTTP_404_NOT_FOUND)

    return data


# GET Visitantes
@router.get('/', response_model=List[VisitanteSchema])
async def get_vistantes(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(VisitanteModel)
        result = await session.execute(query)
        visitantes: List[VisitanteModel] = result.scalars(
        ).unique().all()

        return visitantes

# GET Visitante ID
@router.get('/{id}', response_model=VisitanteSchema, status_code=status.HTTP_200_OK)
async def get_visitante(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(VisitanteModel).filter(VisitanteModel.id == id)
        result = await session.execute(query)
        visitante: VisitanteModel = result.scalars().unique().one_or_none()

        if visitante:
            return visitante
        else:
            raise HTTPException(detail='Visitante não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT Visitante
@router.put('/{id}', response_model=VisitanteSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_visitante(id: int, visitante: VisitanteSchema,  db: AsyncSession = Depends(get_session),
                           user: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(VisitanteModel).filter(VisitanteModel.id == id)
        result = await session.execute(query)
        visitante_update: VisitanteModel = result.scalars().unique().one_or_none()

        # log registro
        await set_log(LogModel(
            table_name=VisitanteModel.__tablename__,
            action='put',
            reg_old=str(visitante_update),
            reg_new=str(visitante.dict()),
            user_id=user.id,
            log_date=datetime.now()
        ), db)

        if visitante_update:

            if visitante.individuo_id:
                visitante_update.individuo_id = visitante.individuo_id

            if visitante.unidade_id:
                visitante_update.unidade_id = visitante.unidade_id

            if visitante.data_inic:
                visitante_update.data_inic = visitante.data_inic

            if visitante.data_fim:
                visitante_update.data_fim = visitante.data_fim
                
            if visitante.tipo_visita:
                visitante_update.tipo_visita = visitante.tipo_visita

            if visitante.observacao:
                visitante_update.observacao = visitante.observacao

            if visitante.situacao:
                visitante_update.situacao = visitante.situacao

            await session.commit()
            return visitante_update
        else:
            raise HTTPException(detail='Visitante não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)

# DELETE Visitante
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_visitante(id: int,  user: UsuarioModel = Depends(get_current_user),
                              db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(VisitanteModel).filter(VisitanteModel.id == id)
        result = await session.execute(query)
        visitante_delete: VisitanteModel = result.scalars().unique().one_or_none()

        if visitante_delete:
            await session.delete(visitante_delete)
            await session.commit()

            # log registro
            await set_log(LogModel(
                table_name=VisitanteModel.__tablename__,
                action='delete',
                reg_old=str(visitante_delete),
                user_id=user.id,
                log_date=datetime.now()
            ), db)

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Visitante não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


