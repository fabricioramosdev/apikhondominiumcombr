from fastapi import APIRouter


from api.v1.endpoints import usuario

from api.v1.endpoints import condominio
from api.v1.endpoints import predio
from api.v1.endpoints import unidade

from api.v1.endpoints import individuo
from api.v1.endpoints import proprietario
from api.v1.endpoints import domiciliado

from api.v1.endpoints import visitante
from api.v1.endpoints import ocorrencia

from api.v1.endpoints import pacotecorrespondencia

from api.v1.endpoints import configs

from api.v1.endpoints import log


api_router = APIRouter()

api_router.include_router(
    condominio.router, prefix='/condominios', tags=['Condominios'])

api_router.include_router(
    predio.router, prefix='/predios', tags=['Predios'])

api_router.include_router(
    unidade.router, prefix='/unidades', tags=['Unidades'])

api_router.include_router(
    individuo.router, prefix='/individuos', tags=['Individuos'])

api_router.include_router(
    proprietario.router, prefix='/proprietarios', tags=['Proprietarios'])

api_router.include_router(
    domiciliado.router, prefix='/domiciliados', tags=['Domiciliados'])

api_router.include_router(
    visitante.router, prefix='/visitantes', tags=['Visitantes'])

api_router.include_router(
    ocorrencia.router, prefix='/ocorrencias', tags=['Ocorrencias'])

api_router.include_router(
    pacotecorrespondencia.router, prefix='/pacotes', tags=['Pacotes e Correspondências'])

api_router.include_router(
    configs.router, prefix='/configs', tags=['Configs'])

api_router.include_router(
    usuario.router, prefix='/usuarios', tags=['Usuarios'])

api_router.include_router(
    log.router, prefix='/logs', tags=['Logs'])

