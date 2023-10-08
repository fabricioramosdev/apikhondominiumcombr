from datetime import datetime
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.condominio_model import CondominioModel, PredioModel
from models.usuario_model import UsuarioModel
from models.log_model import LogModel

from schemas.condominio_schema import CondominioSchema, PredioSchema


from core.deps import get_session, get_current_user, set_log

router = APIRouter()

# POST Condominio
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CondominioSchema)
async def post_condominio(condominio: CondominioSchema, user: UsuarioModel = Depends(get_current_user),
                          db: AsyncSession = Depends(get_session)):

    data: CondominioModel = CondominioModel(
        cnpj=condominio.cnpj, razao_social=condominio.razao_social,
        nome_fantasia=condominio.nome_fantasia, telefone=condominio.telefone,
        email=condominio.email, endereco=condominio.endereco, complemento=condominio.complemento,
        bairro=condominio.bairro, cidade=condominio.cidade, uf=condominio.uf,
    )

    db.add(data)
    await db.commit()
    
     # log registro
    await set_log(LogModel(
        table_name=CondominioModel.__tablename__,
        action='post',
        reg_new=str(data),
        user_id=user.id,
        log_date=datetime.now()
    ), db)

    return data


# GET Condominios
@router.get('/', response_model=List[CondominioSchema])
async def get_condominios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CondominioModel)
        result = await session.execute(query)
        condominios: List[CondominioModel] = result.scalars().unique().all()

        return condominios


# GET Condominio ID
@router.get('/{id}', response_model=CondominioSchema, status_code=status.HTTP_200_OK)
async def get_condominio(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CondominioModel).filter(CondominioModel.id == id)
        result = await session.execute(query)
        condominio: CondominioModel = result.scalars().unique().one_or_none()

        if condominio:
            return condominio
        else:
            raise HTTPException(detail='Condominio não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT Condominio
@router.put('/{id}', response_model=CondominioSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_condominio(id: int, condominio: CondominioSchema,  db: AsyncSession = Depends(get_session),
                         user: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(CondominioModel).filter(CondominioModel.id == id)
        result = await session.execute(query)
        condominio_update: CondominioModel = result.scalars().unique().one_or_none()
        
        # log registro
        await set_log(LogModel(
                table_name=CondominioModel.__tablename__,
                action='put',
                reg_old=str(condominio_update),
                reg_new=str(condominio.dict()),
                user_id=user.id,
                log_date=datetime.now()
            ), db)
                
        if condominio_update:
            if condominio.cnpj:
                condominio_update.cnpj = condominio.cnpj
                
            if condominio.razao_social:
                condominio_update.razao_social = condominio.razao_social
                
            if condominio.nome_fantasia:
                condominio_update.nome_fantasia = condominio.nome_fantasia
                
            if condominio.telefone:
                condominio_update.telefone = condominio.telefone
                
            if condominio.email:
                condominio_update.email = condominio.email
                
            if condominio.endereco:
                condominio_update.endereco = condominio.endereco
                
            if condominio.complemento:
                condominio_update.complemento =  condominio.complemento
                
            if condominio.bairro:
                condominio_update.bairro = condominio.bairro
                
            if condominio.cidade:
                condominio_update.cidade =  condominio.cidade
                
            if condominio.uf:
                condominio_update.uf =  condominio.uf
            
            await session.commit()         
        
            return condominio_update
        else:
            raise HTTPException(detail='Condominio não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE Condominio
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_condominio(id: int,  user: UsuarioModel = Depends(get_current_user),
                            db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CondominioModel).filter(CondominioModel.id == id)
        result = await session.execute(query)
        condominio_delete: CondominioModel = result.scalars().unique().one_or_none()

        if condominio_delete:
            await session.delete(condominio_delete)
            await session.commit()
            
             # log registro
            await set_log(LogModel(
                table_name=CondominioModel.__tablename__,
                action='delete',
                reg_old=str(condominio_delete),
                user_id=user.id,
                log_date=datetime.now()
            ), db)

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Condominio não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
