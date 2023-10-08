from datetime import datetime
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.domiciliado_model import DomiciliadoModel    
from models.usuario_model import UsuarioModel
from models.log_model import LogModel

from schemas.domiciliado_schema import DomiciliadoSchema

from core.deps import get_session, get_current_user, set_log

router = APIRouter()

# POST Domiciliado
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=DomiciliadoSchema)
async def post_domiciliado(domiciliado: DomiciliadoSchema, user: UsuarioModel = Depends(get_current_user),
                            db: AsyncSession = Depends(get_session)):

    try:
        data: DomiciliadoModel = DomiciliadoModel(
            individuo_id=domiciliado.individuo_id,
            unidade_id=domiciliado.unidade_id,
            data_inic=domiciliado.data_inic,
            data_fim=domiciliado.data_fim,
            proprietario=domiciliado.proprietario,
            observacao=domiciliado.observacao,
            situacao=domiciliado.situacao,
        )

        db.add(data)
        await db.commit()

        # log registro
        await set_log(LogModel(
            table_name=DomiciliadoModel.__tablename__,
            action='post',
            reg_new=str(domiciliado.dict()),
            user_id=user.id,
            log_date=datetime.now()
        ), db)

    except exc.IntegrityError:
        raise HTTPException(detail='Dados não encontrados',
                            status_code=status.HTTP_404_NOT_FOUND)

    return data


# GET Domiciliados
@router.get('/', response_model=List[DomiciliadoSchema])
async def get_domiciliados(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(DomiciliadoModel)
        result = await session.execute(query)
        proprietarios: List[DomiciliadoModel] = result.scalars(
        ).unique().all()

        return proprietarios

# GET Domiciliado ID
@router.get('/{id}', response_model=DomiciliadoSchema, status_code=status.HTTP_200_OK)
async def get_domiciliado(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(DomiciliadoModel).filter(DomiciliadoModel.id == id)
        result = await session.execute(query)
        domiciliado: DomiciliadoModel = result.scalars().unique().one_or_none()

        if domiciliado:
            return domiciliado
        else:
            raise HTTPException(detail='Domiciliado não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT Domiciliado
@router.put('/{id}', response_model=DomiciliadoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_domiciliado(id: int, domiciliado: DomiciliadoSchema,  db: AsyncSession = Depends(get_session),
                           user: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(DomiciliadoModel).filter(DomiciliadoModel.id == id)
        result = await session.execute(query)
        domiciliado_update: DomiciliadoModel = result.scalars().unique().one_or_none()

        # log registro
        await set_log(LogModel(
            table_name=DomiciliadoModel.__tablename__,
            action='put',
            reg_old=str(domiciliado_update),
            reg_new=str(domiciliado.dict()),
            user_id=user.id,
            log_date=datetime.now()
        ), db)

        if domiciliado_update:

            if domiciliado.individuo_id:
                domiciliado_update.individuo_id = domiciliado.individuo_id

            if domiciliado.unidade_id:
                domiciliado_update.unidade_id = domiciliado.unidade_id

            if domiciliado.data_inic:
                domiciliado_update.data_inic = domiciliado.data_inic

            if domiciliado.data_fim:
                domiciliado_update.data_fim = domiciliado.data_fim
                
            if domiciliado.proprietario:
                domiciliado_update.proprietario = domiciliado.proprietario

            if domiciliado.observacao:
                domiciliado_update.observacao = domiciliado.observacao

            if domiciliado.situacao:
                domiciliado_update.situacao = domiciliado.situacao

            await session.commit()
            return domiciliado_update
        else:
            raise HTTPException(detail='Domiciliado não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)

# DELETE Domiciliado
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_domiciliado(id: int,  user: UsuarioModel = Depends(get_current_user),
                              db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(DomiciliadoModel).filter(DomiciliadoModel.id == id)
        result = await session.execute(query)
        domiciliado_delete: DomiciliadoModel = result.scalars().unique().one_or_none()

        if domiciliado_delete:
            await session.delete(domiciliado_delete)
            await session.commit()

            # log registro
            await set_log(LogModel(
                table_name=DomiciliadoModel.__tablename__,
                action='delete',
                reg_old=str(domiciliado_delete),
                user_id=user.id,
                log_date=datetime.now()
            ), db)

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Domiciliado não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
