from datetime import datetime
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import exc

from models.condominio_model import CondominioModel, PredioModel, UnidadeModel
from models.usuario_model import UsuarioModel
from models.log_model import LogModel

from schemas.condominio_schema import UnidadeSchema
from schemas.display_value_schema import DiplayValueSchema

from core.deps import get_session, get_current_user, set_log


router = APIRouter()

# POST Unidade


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UnidadeSchema)
async def post_unidade(unidade: UnidadeSchema, user: UsuarioModel = Depends(get_current_user),
                       db: AsyncSession = Depends(get_session)):

    data: UnidadeModel = UnidadeModel(
        uuid=unidade.uuid,
        predio_id=unidade.predio_id,
        observacao=unidade.observacao
    )

    db.add(data)
    await db.commit()

    # log registro
    await set_log(LogModel(
        table_name=UnidadeModel.__tablename__,
        action='post',
        reg_new=str(unidade.dict()),
        user_id=user.id,
        log_date=datetime.now()
    ), db)

    return data


# GET Unidade
@router.get('/', response_model=List[UnidadeSchema])
async def get_unidade(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UnidadeModel)
        result = await session.execute(query)
        unidades: List[UnidadeModel] = result.scalars().unique().all()

        return unidades


# GET Unidade ID
@router.get('/{id}', response_model=UnidadeSchema, status_code=status.HTTP_200_OK)
async def get_unidade(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UnidadeModel).filter(UnidadeModel.id == id)
        result = await session.execute(query)
        unidade: UnidadeModel = result.scalars().unique().one_or_none()

        if unidade:
            return unidade
        else:
            raise HTTPException(detail='Unidade não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)

# GET Unidades Predio ID
@router.get('/predio/{id}', response_model=List[UnidadeSchema], status_code=status.HTTP_200_OK)
async def get_unidades_predio(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:

        query = select(UnidadeModel).join(PredioModel,
                                          UnidadeModel.predio_id == PredioModel.id).filter(UnidadeModel.predio_id == id)

        result = await session.execute(query)
        unidades: List[UnidadeModel] = result.scalars().unique().all()

        return unidades


# GET Unidades Condominio ID
@router.get('/condominio/{id}', response_model=List[UnidadeSchema], status_code=status.HTTP_200_OK)
async def get_unidades_condominio(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:

        query = select(UnidadeModel).join(PredioModel,
                                          UnidadeModel.predio_id == PredioModel.id).join(CondominioModel,
                                                                                         PredioModel.condominio_id == CondominioModel.id).filter(CondominioModel.id == id)
        result = await session.execute(query)

        unidades: List[UnidadeModel] = result.scalars().unique().all()

        return unidades



# PUT Unidade
@router.put('/{id}', response_model=UnidadeSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_unidade(id: int, unidade: UnidadeSchema,  db: AsyncSession = Depends(get_session),
                      user: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(UnidadeModel).filter(UnidadeModel.id == id)
        result = await session.execute(query)
        unidade_update: UnidadeModel = result.scalars().unique().one_or_none()

        # log registro
        await set_log(LogModel(
            table_name=UnidadeModel.__tablename__,
            action='put',
            reg_old=str(unidade_update),
            reg_new=str(unidade.dict()),
            user_id=user.id,
            log_date=datetime.now()
        ), db)

        if unidade_update:
            if unidade.uuid:
                unidade_update.uuid = unidade.uuid
            if unidade.predio_id:
                unidade_update.predio_id = unidade.predio_id
            if unidade.observacao:
                unidade_update.observacao = unidade.observacao

            await session.commit()

            return unidade_update
        else:
            raise HTTPException(detail='Unidade não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE Unidade
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_unidade(id: int,  user: UsuarioModel = Depends(get_current_user),
                         db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UnidadeModel).filter(UnidadeModel.id == id)
        result = await session.execute(query)
        unidade_delete: UnidadeModel = result.scalars().unique().one_or_none()

        if unidade_delete:
            await session.delete(unidade_delete)
            await session.commit()

            # log registro
            await set_log(LogModel(
                table_name=UnidadeModel.__tablename__,
                action='delete',
                reg_old=str(unidade_delete),
                user_id=user.id,
                log_date=datetime.now()
            ), db)

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Unidade não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
