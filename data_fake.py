import requests
import json

from datetime import datetime

# passo 01 - 201


def post_usuario(usuario):
    """
    Makes a POST request to a web API endpoint to create a new user.

    Args:
        usuario (dict): A dictionary containing information about the user. It should have the keys 'nome', 'email', and 'senha'.

    Returns:
        int: The status code of the response from the API.

    Example Usage:
        usuario = {'nome': 'John Doe', 'email': 'john.doe@example.com', 'senha': 'password'}
        response = post_usuario(usuario)
        print(response)  # 201
    """
    headers = {'Content-type': 'application/json'}
    response = requests.post(
        'http://localhost:8000/api/v1/usuarios/signup', data=json.dumps(usuario), headers=headers)
    print(f'(201) Passo 01: {response.status_code}')
    return response.status_code

# passo 02 - 200


def login_usuario(login):

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = login

    response = requests.post(
        'http://localhost:8000/api/v1/usuarios/login', headers=headers, data=data)
    print(f'(200) Passo 02: {response.status_code}')
    return response.text

# passo 03 - 200


def post_condominio(condominio, prefix, token):

    token = f'{prefix} {token}'
    headers = {
        'accept': 'application/json',
        f'Authorization': token,
        'Content-Type': 'application/json',
    }

    response = requests.post(
        'http://localhost:8000/api/v1/condominios/', headers=headers, json=condominio)
    print(f'(201) Passo 03: {response.status_code}')
    return response.text

# passo 4 - 200


def post_predios(predios, prefix, token):

    token = f'{prefix} {token}'
    headers = {
        'accept': 'application/json',
        f'Authorization': token,
        'Content-Type': 'application/json',
    }

    response = requests.post(
        'http://localhost:8000/api/v1/predios/', headers=headers, json=predios)
    print(f'(201) Passo 04: {response.status_code}')
    return response.text


# passo 5 - 200
def post_unidades(unidade, prefix, token):
    """
    Make a POST request to the '/api/v1/unidades/' endpoint of a web API.

    Args:
        unidade (dict): A dictionary containing information about a unit. It should have the keys 'uuid' and 'predio_id'.
        prefix (str): The prefix to be used in the authorization token. For example, 'Bearer'.
        token (str): The authorization token to be included in the request headers.

    Returns:
        str: The response text from the API, which contains information about the created unit.
    """
    token = f'{prefix} {token}'
    headers = {
        'accept': 'application/json',
        f'Authorization': token,
        'Content-Type': 'application/json',
    }

    response = requests.post(
        'http://localhost:8000/api/v1/unidades/', headers=headers, json=unidade)
    print(f'(201) Passo 05: {response.status_code}')
    return response.text

# passo 6 - 200


def post_individuos(individuo, prefix, token):
    token = f'{prefix} {token}'
    headers = {
        'accept': 'application/json',
        f'Authorization': token,
        'Content-Type': 'application/json',
    }

    response = requests.post(
        'http://localhost:8000/api/v1/individuos/', headers=headers, json=individuo)
    print(f'(201) Passo 06: {response.status_code}')
    return response.text

# passo 7 - 200


def post_proprietarios(proprietario, prefix, token):
    token = f'{prefix} {token}'
    headers = {
        'accept': 'application/json',
        f'Authorization': token,
        'Content-Type': 'application/json',
    }

    response = requests.post(
        'http://localhost:8000/api/v1/proprietarios/', headers=headers, json=proprietario)
    print(f'(201) Passo 07: {response.status_code}')
    return response.text


# passo 8 - 200
def post_domiciliados(domiciliado, prefix, token):
    token = f'{prefix} {token}'
    headers = {
        'accept': 'application/json',
        f'Authorization': token,
        'Content-Type': 'application/json',
    }

    response = requests.post(
        'http://localhost:8000/api/v1/domiciliados/', headers=headers, json=domiciliado)
    print(f'(201) Passo 08: {response.status_code}')
    return response.text


# passo 9 - 200
def post_visitantes(visitante, prefix, token):
    token = f'{prefix} {token}'
    headers = {
        'accept': 'application/json',
        f'Authorization': token,
        'Content-Type': 'application/json',
    }

    response = requests.post(
        'http://localhost:8000/api/v1/visitantes/', headers=headers, json=visitante)
    print(f'(201) Passo 09: {response.status_code}')
    return response.text


# passo 10 - 200
def post_ocorrencias(ocorrencia, prefix, token):
    token = f'{prefix} {token}'
    headers = {
        'accept': 'application/json',
        f'Authorization': token,
        'Content-Type': 'application/json',
    }

    response = requests.post(
        'http://localhost:8000/api/v1/ocorrencias/', headers=headers, json=ocorrencia)
    print(f'(201) Passo 10: {response.status_code}')
    return response.text


# passo 11 - 200

def post_pacotes_correspondencias(pacote_correspondencia, prefix, token):
    token = f'{prefix} {token}'
    headers = {
        'accept': 'application/json',
        f'Authorization': token,
        'Content-Type': 'application/json',
    }

    response = requests.post(
        'http://localhost:8000/api/v1/pacotes/', headers=headers, json=pacote_correspondencia)
    print(f'(201) Passo 11: {response.status_code}')
    return response.text


if __name__ == '__main__':

    from criar_tabelas import create_tables
    import asyncio

    asyncio.run(create_tables())


    fake1 = post_usuario({

        'nome': "Fabricio Rogério Lopes",
        'sobrenome': "Ramos",
        'email': "fabricio.ramos.dev@gmail.com",
        'eh_admin': True,
        'senha': "pri142407"
    })

    if fake1 == 201:
        fake2 = login_usuario({
            'username': "fabricio.ramos.dev@gmail.com",
            'password': "pri142407"
        })
        access = json.loads(fake2)

        condominios = [{
            'cnpj': '187260001-1',
            'razao_social': 'Parque Bavaria',
            'nome_fantasia': 'Bavaria',
            'telefone': '(14)9999-9999',
            'email': 'parquebavaria.sindico@bavaria.com.br',
            'endereco': 'Rua Dr. José Barbosa de Barros, 1630 ',
            'complemento': 'Terceira caixa de agua da rua',
            'bairro': 'Jd. Paraíso',
            'cidade': 'Botucatu',
            'uf': 'SP',
        }, {
            'cnpj': '2177452445-1',
            'razao_social': 'Parque Baltimore',
            'nome_fantasia': 'Baltimore',
            'telefone': '(14)7777-777',
            'email': 'parquebaltimore.sindico@bavaria.com.br',
            'endereco': 'Rua Dr. José Barbosa de Barros, 1530 ',
            'bairro': 'Jd. Paraíso',
            'cidade': 'Botucatu',
            'uf': 'SP',
        }]

        for condominio in condominios:
            fake3 = post_condominio(condominio, access.get(
                'token_type'), access.get('access_token'))

        predios = [{
            'uuid': 'Bloco 1',
            'condominio_id': 1,
            'observacao': 'Bloco'
        }, {
            'uuid': 'Bloco 2',
            'condominio_id': 1,
            'observacao': 'Bloco'
        }, {
            'uuid': 'Bloco 3',
            'condominio_id': 1,
            'observacao': 'Bloco'
        }, {
            'uuid': 'Bloco 4',
            'condominio_id': 1,
            'observacao': 'Bloco'
        }, {
            'uuid': 'Bloco 1',
            'condominio_id': 2,
            'observacao': 'Bloco'
        }, {
            'uuid': 'Bloco 2',
            'condominio_id': 2,
            'observacao': 'Bloco'
        }, {
            'uuid': 'Bloco 3',
            'condominio_id': 2,
            'observacao': 'Bloco'
        }]

        for predio in predios:

            fake4 = post_predios(predio, access.get(
                'token_type'), access.get('access_token'))

        unidades = [{'uuid': '101', 'predio_id': 1}, {'uuid': '102', 'predio_id': 1}, {'uuid': '103', 'predio_id': 1},
                    {'uuid': '201', 'predio_id': 2}, {'uuid': '202',
                                                      'predio_id': 2}, {'uuid': '203', 'predio_id': 2},
                    {'uuid': '301', 'predio_id': 3, 'observacao': 'Apartamento de um quarto'}, {
                        'uuid': '302', 'predio_id': 3},
                    {'uuid': '303', 'predio_id': 3}, {'uuid': '101',
                                                      'predio_id': 6}, {'uuid': '102', 'predio_id': 6},
                    {'uuid': '103', 'predio_id': 6}, {'uuid': '104',
                                                      'predio_id': 6}, {'uuid': '105', 'predio_id': 6},
                    {'uuid': '106', 'predio_id': 6}, {'uuid': '101',
                                                      'predio_id': 5}, {'uuid': '101', 'predio_id': 5},
                    {'uuid': '105', 'predio_id': 7}]
        
        for unidade in unidades:
            fake5 = post_unidades(unidade, access.get(
                'token_type'), access.get('access_token'))

        individuos = [
            {
                'nome': 'Fabrício Rogério Lopes Ramos',
                'cpf': '311.136.588-35',
                'rg': '42.236.867-2',
                'data_nasc': '1985-07-14',
                'celular': '(14)99618-1322',
                'email': 'fabricio.ramos.dev@gmail.com',
                'condominio_id': 1
            },
            {
                'nome': 'Daiane Priscila de Camargo',
                'cpf': '419.610.168-32',
                'data_nasc': '1993-07-24',
                'celular': '(14)99762-49912',
                'email': 'daiane.pricamargo@gmail.com',
                'condominio_id': 1
            },
            {
                'nome': 'Fabrício Rogério Lopes Ramos',
                'cpf': '311.136.588-35',
                'rg': '42.236.867-2',
                'data_nasc': '1985-07-14',
                'celular': '(14)99618-1322',
                'email': 'fabricio.ramos.dev@gmail.com',
                'condominio_id': 2
            },
            {
                'nome': 'Fabrício Rogério Lopes Ramos',
                'cpf': '311.136.588-35',
                'rg': '42.236.867-2',
                'data_nasc': '1985-07-14',
                'celular': '(14)99618-1322',
                'email': 'fabricio.ramos.dev@gmail.com',
                'condominio_id': 1
            }

        ]

        for individuo in individuos:
            fake6 = post_individuos(individuo, access.get(
                'token_type'), access.get('access_token'))

        proprietarios = [{
            'individuo_id': 1,
            'unidade_id': 8,
        }, {
            'individuo_id': 2,
            'unidade_id': 1,
        }, {
            'individuo_id': 2,
            'unidade_id': 4,
        }, {
            'individuo_id': 1,
            'unidade_id': 3,
            'data_inic': '2012-04-19'
        }, {
            'individuo_id': 1,
            'unidade_id': 6,
            'data_inic': '2012-04-19',
            'data_fim': '2023-07-20',
            'situacao': False
        }, {
            'individuo_id': 2,
            'unidade_id': 6,
            'data_inic': '2023-07-20'
        }, {
            'individuo_id': 3,
            'unidade_id': 8,
            'data_inic': '2023-07-20'
        }, {
            'individuo_id': 3,
            'unidade_id': 10,
            'data_inic': '2023-07-20'
        }, {
            'individuo_id': 3,
            'unidade_id': 10,
            'data_inic': '2023-07-20'
        }, {
            'individuo_id': 3,
            'unidade_id': 11,
            'data_inic': '2023-07-20'
        }]
        for proprietario in proprietarios:
            fake7 = post_proprietarios(
                proprietario, access.get(
                    'token_type'), access.get('access_token')
            )

        domiciliados = [{
            'individuo_id': 1,
            'unidade_id': 8,
            'proprietario': True
        }, {
            'individuo_id': 2,
            'unidade_id': 8,
            'data_inic': '2012-04-19',
            'observacao': 'Moradora esposa do proprietário'
        }]
        for domiciliado in domiciliados:
            fake8 = post_domiciliados(domiciliado, access.get(
                'token_type'), access.get('access_token'))

        visitantes = [{
            'individuo_id': 1,
            'unidade_id': 8,
            'tipo_visita': 'servicos'
        }, {
            'individuo_id': 2,
            'unidade_id': 1,
            'tipo_visita': 'hospede'
        }, {
            'individuo_id': 2,
            'unidade_id': 4,
        }, {
            'individuo_id': 1,
            'unidade_id': 3,
            'data_inic': '2012-04-19 10:24:12'
        }, {
            'individuo_id': 1,
            'unidade_id': 6,
            'data_inic': '2012-03-19 07:35:00',
            'data_fim': '2023-03-19 08:40:00',
            'situacao': False
        }, {
            'individuo_id': 2,
            'unidade_id': 6,
            'data_inic': '2023-07-20 15:10:00'
        }]
        for visitante in visitantes:
            fake9 = post_visitantes(visitante, access.get(
                'token_type'), access.get('access_token'))

    ocorrencias = [
        {

            "unidade_id": 1,
            "tipo_ocorrencia": "notificação",
            "notificar_ocorrencia": "não notificar",
            "data_fato": str(datetime.now()),
            "dsc_fato": "Notificação 01",
            "situacao": True
        }, {

            "unidade_id": 8,
            "tipo_ocorrencia": "notificação",
            "notificar_ocorrencia": "não notificar",
            "data_fato": str(datetime.now()),
            "dsc_fato": "Notificação 08",

            "situacao": True
        }, {

            "unidade_id": 3,
            "tipo_ocorrencia": "notificação",
            "notificar_ocorrencia": "notificar inquilino",
            "data_fato": str(datetime.now()),
            "dsc_fato": "Notificação 03",

            "situacao": True
        }, {

            "unidade_id": 5,
            "tipo_ocorrencia": "notificação",
            "notificar_ocorrencia": "notificar proprietário",
            "data_fato": str(datetime.now()),
            "dsc_fato": "Notificação 05",
            "dsc_conclusao": "Notificação 8 foi resolvida com o proprietário do apartamento",
            "situacao": False
        },
        {

            "unidade_id": 8,
            "tipo_ocorrencia": "notificação",
            "notificar_ocorrencia": "notificar proprietário",
            "data_fato": str(datetime.now()),
            "dsc_fato": "Notificação 08",
            "situacao": True
        },
        {

            "unidade_id": 10,
            "tipo_ocorrencia": "notificação",
            "notificar_ocorrencia": "notificar proprietário",
            "data_fato": str(datetime.now()),
            "dsc_fato": "Notificação 10",
            "situacao": True
        },
        {

            "unidade_id": 11,
            "tipo_ocorrencia": "notificação",
            "notificar_ocorrencia": "notificar proprietário",
            "data_fato": str(datetime.now()),
            "dsc_fato": "Notificação 11",
            "situacao": True
        }]

    for ocorrencia in ocorrencias:
        fake10 = post_ocorrencias(ocorrencia, access.get(
            'token_type'), access.get('access_token'))

    pacotes_correspondencias = [
        {
            "unidade_id": 1,
            "destinatario": "Ana Laura  de Camargo 1",
            "objeto": "RASTREIO",
            "responsavel_recebimento": 1,
            "data_recebimento": "2023-10-05",
        },
        {
            "unidade_id": 1,
            "destinatario": "Daiane Priscila de Camargo 1",
            "objeto": "RASTREIO",
            "responsavel_recebimento": 1,
            "data_recebimento": "2023-10-07",
        },
        {
            "unidade_id": 10,
            "destinatario": "Daiane Priscila de Camargo 10",
            "objeto": "RASTREIO",
            "responsavel_recebimento": 1,
            "data_recebimento": "2023-10-07",
        },
        {
            "unidade_id": 14,
            "destinatario": "Fabricio Rogerio Lopes Ramos 14",
            "objeto": "RASTREIO",
            "responsavel_recebimento": 1,
            "data_recebimento": "2023-10-07",
        },
    ]
    for pacote_correspondencia in pacotes_correspondencias:
        fake11 = post_pacotes_correspondencias(pacote_correspondencia, access.get(
            'token_type'), access.get('access_token'))
