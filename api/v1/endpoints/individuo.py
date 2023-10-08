import re
from datetime import datetime
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.condominio_model import IndividuoModel
from models.usuario_model import UsuarioModel
from models.log_model import LogModel

from schemas.condominio_schema import IndividuoSchema, IndividuoPutSchema

from core.deps import get_session, get_current_user, set_log


router = APIRouter()


           

def remove_dots_from_documents(cpf):
    # Remove all dot characters from the dpcuments
    cpf_without_dots = re.sub(r"\D", "", cpf)
    return cpf_without_dots


# POST Individuo
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=IndividuoSchema)
async def post_individuo(individuo: IndividuoSchema, user: UsuarioModel = Depends(get_current_user),
                         db: AsyncSession = Depends(get_session)):
    try:

        data: IndividuoModel = IndividuoModel(
            nome=individuo.nome,
            cpf=remove_dots_from_documents(
                individuo.cpf) if individuo.cpf else None,
            rg=remove_dots_from_documents(
                individuo.rg) if individuo.rg else None,
            data_nasc=individuo.data_nasc,
            genero=individuo.genero,
            telefone=individuo.telefone,
            celular=individuo.celular,
            email=individuo.email,
            cep=individuo.cep,
            endereco=individuo.endereco,
            complemento=individuo.complemento,
            bairro=individuo.bairro,
            cidade=individuo.cidade,
            estado=individuo.estado,
            observacao=individuo.observacao,
            situacao=individuo.situacao,
            condominio_id=individuo.condominio_id
        )
    

        db.add(data)
        await db.commit()
        
    except exc.IntegrityError as e:  

        raise HTTPException(detail=f'Individuo com CPF {individuo.cpf} já registrado',
                            status_code=status.HTTP_404_NOT_FOUND)

     # log registro
    await set_log(LogModel(
        table_name=IndividuoModel.__tablename__,
        action='post',
        reg_new=str(individuo.dict()),
        user_id=user.id,
        log_date=datetime.now()
    ), db)

    return data

# GET Individuos


@router.get('/', response_model=List[IndividuoSchema])
async def get_individuos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(IndividuoModel)
        result = await session.execute(query)
        individuos: List[IndividuoModel] = result.scalars().unique().all()

        return individuos


# GET Individuo ID
@router.get('/{id}', response_model=IndividuoSchema, status_code=status.HTTP_200_OK)
async def get_unidade(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(IndividuoModel).filter(IndividuoModel.id == id)
        result = await session.execute(query)
        unidade: IndividuoModel = result.scalars().unique().one_or_none()

        if unidade:
            return unidade
        else:
            raise HTTPException(detail='Individuo não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)


# GET Individuo Condominio ID
@router.get('/condominio/{id}', response_model=List[IndividuoSchema], status_code=status.HTTP_200_OK)
async def get_unidade_condominio(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(IndividuoModel).filter(
            IndividuoModel.condominio_id == id)
        result = await session.execute(query)
        individuos: List[IndividuoSchema] = result.scalars().unique().all()

        if individuos:
            return individuos
        else:
            raise HTTPException(detail='Individuo não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT Individuo

@router.put('/{id}', response_model=IndividuoPutSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_individuo(id: int, individuo: IndividuoPutSchema,  db: AsyncSession = Depends(get_session),
                        user: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(IndividuoModel).filter(IndividuoModel.id == id)
        result = await session.execute(query)
        individuo_update: IndividuoModel = result.scalars().unique().one_or_none()

        # log registro
        await set_log(LogModel(
            table_name=IndividuoModel.__tablename__,
            action='put',
            reg_old=str(individuo_update),
            reg_new=str(individuo.dict()),
            user_id=user.id,
            log_date=datetime.now()
        ), db)

        if individuo_update:
            if individuo.nome:
                individuo_update.nome = individuo.nome
            if individuo.cpf:
                individuo_update.cpf = individuo.cpf
            if individuo.rg:
                individuo_update.rg = individuo.rg
            if individuo.data_nasc:
                individuo_update.data_nasc = individuo.data_nasc
            if individuo.genero:
                individuo_update.genero = individuo.genero
            if individuo.telefone:
                individuo_update.telefone = individuo.telefone
            if individuo.celular:
                individuo_update.celular = individuo.celular
            if individuo.email:
                individuo_update.email = individuo.email
            if individuo.cep:
                individuo_update.cep = individuo.cep
                individuo_update.endereco = individuo.endereco
            if individuo.complemento:
                individuo_update.complemento = individuo.complemento
            if individuo.bairro:
                individuo_update.bairro = individuo.bairro
            if individuo.cidade:
                individuo_update.cidade = individuo.cidade
            if individuo.estado:
                individuo_update.estado = individuo.estado
            if individuo.observacao:
                individuo_update.observacao = individuo.observacao
            if individuo.situacao:
                individuo_update.situacao = individuo.situacao

            if individuo.condominio_id:
                individuo_update.condominio_id = individuo.condominio_id

            await session.commit()

            return individuo_update
        else:
            raise HTTPException(detail='Individuo não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)

# DELETE Individuo


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_individuo(id: int,  user: UsuarioModel = Depends(get_current_user),
                           db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(IndividuoModel).filter(IndividuoModel.id == id)
        result = await session.execute(query)
        individuo_delete: IndividuoModel = result.scalars().unique().one_or_none()

        if individuo_delete:
            await session.delete(individuo_delete)
            await session.commit()

            # log registro
            await set_log(LogModel(
                table_name=IndividuoModel.__tablename__,
                action='delete',
                reg_old=str(individuo_delete),
                user_id=user.id,
                log_date=datetime.now()
            ), db)

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Individuo não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
