
from datetime import datetime
from typing import List


from enum import Enum

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.pacote_correspondencia_model import PacoteCorrespondeciaModel
from models.condominio_model import (UnidadeModel,
                                     PredioModel)
from models.usuario_model import UsuarioModel
from models.log_model import LogModel

from schemas.pacote_correspondencia_schema import PacoteCorrespondeciaSchema

from core.deps import get_session, get_current_user, set_log

router = APIRouter()

# POST Pacotes e Correspondencias


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PacoteCorrespondeciaSchema)
async def post_pacote_correspondencia(pacote_correspondencia: PacoteCorrespondeciaSchema, user: UsuarioModel = Depends(get_current_user),
                                      db: AsyncSession = Depends(get_session)):

    try:

        data: PacoteCorrespondeciaModel = PacoteCorrespondeciaModel(
            unidade_id=pacote_correspondencia.unidade_id,
            destinatario=pacote_correspondencia.destinatario,
            objeto=pacote_correspondencia.objeto,
            responsavel_recebimento=user.id if pacote_correspondencia.responsavel_recebimento is None else pacote_correspondencia.responsavel_recebimento,
            data_recebimento=pacote_correspondencia.data_recebimento,
            responsavel_retirada=pacote_correspondencia.responsavel_retirada,
            retirado_por=pacote_correspondencia.retirado_por,
            num_doc=pacote_correspondencia.num_doc,
            data_retirada=pacote_correspondencia.data_retirada,
            situacao=pacote_correspondencia.situacao
        )

        db.add(data)
        await db.commit()

        # log registro
        await set_log(LogModel(
            table_name=PacoteCorrespondeciaModel.__tablename__,
            action='post',
            reg_new=str(pacote_correspondencia.dict()),
            user_id=user.id,
            log_date=datetime.now()
        ), db)

    except exc.IntegrityError:
        raise HTTPException(detail='Dados não encontrados',
                            status_code=status.HTTP_404_NOT_FOUND)

    return data

# GET Pacotes e Correspondencias


@router.get('/', response_model=List[PacoteCorrespondeciaSchema])
async def get_pacotes_correspondencias(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PacoteCorrespondeciaModel)
        result = await session.execute(query)
        pacotes_correspondencias: List[PacoteCorrespondeciaModel] = result.scalars(
        ).unique().all()

        return pacotes_correspondencias


# GET Pacote e Correspondecia ID
@router.get('/{id}', response_model=PacoteCorrespondeciaSchema, status_code=status.HTTP_200_OK)
async def get_pacote_correspondencia(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PacoteCorrespondeciaModel).filter(
            PacoteCorrespondeciaModel.id == id)
        result = await session.execute(query)
        pacote_correspondencia: PacoteCorrespondeciaModel = result.scalars().unique().one_or_none()

        if pacote_correspondencia:
            return pacote_correspondencia
        else:
            raise HTTPException(detail='Pacote/Correspondencia não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)


# GET Pacotes e Correspondencias Condominio ID
@router.get('/condominio/{id}', response_model=List[PacoteCorrespondeciaSchema], status_code=status.HTTP_200_OK)
async def get_pacotes_correspondencias_condoninio(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PacoteCorrespondeciaModel).join(
            UnidadeModel, UnidadeModel.id == PacoteCorrespondeciaModel.unidade_id
        ).join(PredioModel, PredioModel.id == UnidadeModel.predio_id).filter(PredioModel.condominio_id==id)
        result = await session.execute(query)
        pacotes_correspondencias : List[PacoteCorrespondeciaSchema] = result.scalars().unique().all()

        if pacotes_correspondencias:
            return pacotes_correspondencias
        else:
            raise HTTPException(detail='Pacotes/Correspondencias não encontrados',
                                status_code=status.HTTP_404_NOT_FOUND)

    
    
    
# PUT Pacotes e Correspondencias
@router.put('/{id}', response_model=PacoteCorrespondeciaSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_pacote_correspondencia(id: int, pacote_correspondencia: PacoteCorrespondeciaSchema,  db: AsyncSession = Depends(get_session),
                                     user: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(PacoteCorrespondeciaModel).filter(
            PacoteCorrespondeciaModel.id == id)
        result = await session.execute(query)
        pacote_correspondencia_update: PacoteCorrespondeciaModel = result.scalars(
        ).unique().one_or_none()

        # log registro
        await set_log(LogModel(
            table_name=PacoteCorrespondeciaModel.__tablename__,
            action='put',
            reg_old=str(pacote_correspondencia_update),
            reg_new=str(pacote_correspondencia.dict()),
            user_id=user.id,
            log_date=datetime.now()
        ), db)

        if pacote_correspondencia_update:

            if pacote_correspondencia.unidade_id:
                pacote_correspondencia_update.unidade_id = pacote_correspondencia.unidade_id

            if pacote_correspondencia.destinatario:
                pacote_correspondencia_update.destinatario = pacote_correspondencia.destinatario

            if pacote_correspondencia.objeto:
                pacote_correspondencia_update.objeto = pacote_correspondencia.objeto

            if pacote_correspondencia.responsavel_recebimento:
                pacote_correspondencia_update.responsavel_recebimento = pacote_correspondencia.responsavel_recebimento

            if pacote_correspondencia.data_recebimento:
                pacote_correspondencia_update.data_recebimento = pacote_correspondencia.data_recebimento

            if pacote_correspondencia.responsavel_retirada:
                pacote_correspondencia_update.responsavel_retirada = pacote_correspondencia.responsavel_retirada

            if pacote_correspondencia.retirado_por:
                pacote_correspondencia_update.retirado_por = pacote_correspondencia.retirado_por

            if pacote_correspondencia.num_doc:
                pacote_correspondencia_update.num_doc = pacote_correspondencia.num_doc

            if pacote_correspondencia.data_retirada:
                pacote_correspondencia_update.data_retirada = pacote_correspondencia.data_retirada

            if pacote_correspondencia.situacao:
                pacote_correspondencia_update.situacao = pacote_correspondencia.situacao

            await session.commit()
            return pacote_correspondencia_update
        else:
            raise HTTPException(detail='Pacote/Correspondencia não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE Pacotes e Correspondencias
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_pacote_correspondencia(id: int,  user: UsuarioModel = Depends(get_current_user),
                              db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(PacoteCorrespondeciaModel).filter(PacoteCorrespondeciaModel.id == id)
        result = await session.execute(query)
        pacote_correspondencia_delete: PacoteCorrespondeciaModel = result.scalars().unique().one_or_none()

        if pacote_correspondencia_delete:
            await session.delete(pacote_correspondencia_delete)
            await session.commit()

            # log registro
            await set_log(LogModel(
                table_name=PacoteCorrespondeciaModel.__tablename__,
                action='delete',
                reg_old=str(pacote_correspondencia_delete),
                user_id=user.id,
                log_date=datetime.now()
            ), db)

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Pacote/Correspondencia não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)

