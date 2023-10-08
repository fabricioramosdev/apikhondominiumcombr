from datetime import datetime
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import exc

from models.condominio_model import PredioModel
from models.usuario_model import UsuarioModel
from models.log_model import LogModel

from schemas.condominio_schema import PredioSchema
from schemas.display_value_schema import DiplayValueSchema


from core.deps import get_session, get_current_user, set_log

router = APIRouter()

# POST Predio
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PredioSchema)
async def post_predio(predio: PredioSchema, user: UsuarioModel = Depends(get_current_user),
                      db: AsyncSession = Depends(get_session)):

    try:

        data: PredioModel = PredioModel(
            uuid=predio.uuid,
            condominio_id=predio.condominio_id,
            observacao=predio.observacao
        )

        db.add(data)
        await db.commit()

        # log registro
        await set_log(LogModel(
            table_name=PredioModel.__tablename__,
            action='post',
            reg_new=str(predio.dict()),
            user_id=user.id,
            log_date=datetime.now()
        ), db)

        return data
    except exc.IntegrityError as e:
        raise HTTPException(detail='Condominio não encontrado',
                            status_code=status.HTTP_404_NOT_FOUND)
    except exc.DatabaseError as e:
        raise HTTPException(detail='Erro interno do servidor',
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# GET Predio
@router.get('/', response_model=List[PredioSchema])
async def get_predios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PredioModel)
        result = await session.execute(query)
        predios: List[PredioModel] = result.scalars().unique().all()
        return predios



# GET Predio ID
@router.get('/{id}', response_model=PredioSchema, status_code=status.HTTP_200_OK)
async def get_predio(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PredioModel).filter(PredioModel.id == id)
        result = await session.execute(query)
        predio: PredioModel = result.scalars().unique().one_or_none()

        if predio:
            return predio
        else:
            raise HTTPException(detail='Predio não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


# GET Predio Condominio IDs
@router.get('/condominio/{id}',response_model=List[PredioSchema])
async def get_predios_condominio(id: int, db: AsyncSession = Depends(get_session)):
       async with db as session:
        query = select(PredioModel).filter(PredioModel.condominio_id == id)
        result = await session.execute(query)
        predio: List[PredioModel] = result.scalars().unique().all() 
        return predio
      



# PUT Predio
@router.put('/{id}', response_model=PredioSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_predio(id: int, predio: PredioSchema,  db: AsyncSession = Depends(get_session),
                         user: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(PredioModel).filter(PredioModel.id == id)
        result = await session.execute(query)
        predio_update: PredioModel = result.scalars().unique().one_or_none()
        
        # log registro
        await set_log(LogModel(
                table_name=PredioModel.__tablename__,
                action='put',
                reg_old=str(predio_update),
                reg_new=str(predio.dict()),
                user_id=user.id,
                log_date=datetime.now()
            ), db)
    

        if predio_update:
            
            if predio.uuid:
                predio_update.uuid = predio.uuid
                
            if predio.condominio_id:
                predio_update.condominio_id = predio.condominio_id
                
            if predio.observacao:
           
                predio_update.observacao = predio.observacao
            
            await session.commit()         
            return predio_update
        else:
            raise HTTPException(detail='Predio não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE Predio
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_predio(id: int,  user: UsuarioModel = Depends(get_current_user),
                            db: AsyncSession = Depends(get_session)):
    

    async with db as session:
        query = select(PredioModel).filter(PredioModel.id == id)
        result = await session.execute(query)
        predio_delete: PredioModel = result.scalars().unique().one_or_none()

        if predio_delete:
            await session.delete(predio_delete)
            await session.commit()
            
             # log registro
            await set_log(LogModel(
                table_name=PredioModel.__tablename__,
                action='delete',
                reg_old=str(predio_delete),
                user_id=user.id,
                log_date=datetime.now()
            ), db)

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Predio não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
