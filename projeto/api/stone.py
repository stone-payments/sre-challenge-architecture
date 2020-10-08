from aiohttp import web
import json
import asyncio
import asyncpg

import redis
from datetime import timedelta

def status(code):
    """Retorna mensagem de status"""
    if code == 200:
        responseObj = {'status' : 'success'}
        response = web.Response(text=json.dumps(responseObj), status=200)
    if code == 406:
        responseObj = {'status' : 'Erro, Algum problema com a syntax'}
        response = web.Response(text=json.dumps(responseObj), status=406)
    if code == 500:
        responseObj = {'status' : 'Error'}
        response = web.Response(text=json.dumps(responseObj), status=500)
    return response

def setUser(obj):
    """Recebe o objeto enviado pelo post e retorna em formato de dicionario"""
    user = {}
    for key, value in obj.items():
        if key == "nome":
            user[key] = value
        elif key == "sobrenome":
            user[key] = value
        elif key == "cpf":
            if len(value) == 11:
                user[key] = value
            else:
                return "err"
        elif key == "bday":
            if len(value) == 8:
                user[key] = value
            else:
                return "err"
        else:
            status(406)
    return user

routes = web.RouteTableDef()

@routes.get('/')
async def get_handler(request):
    """Retorna somento ok"""
    return status(200)

@routes.post('/post')
async def post_handler(request):
    """nome, sobrenome, cpf, data de nascimento"""
    result = setUser(request.headers)
    if result:
        """Handle incoming requests."""
        pool = request.app['pool']
        async with pool.acquire() as connection:
            async with connection.transaction():
                try:
                    results = await connection.fetch('insert into users (name,lastname,cpf,bday)\
                        values (\'{name}\', \'{lastname}\',\'{cpf}\',\'{bday}\')'.format(name=result['nome'], lastname=result['sobrenome'],\
                            cpf=result['cpf'],bday=result['bday']))
                    statusResult = { 'Status' : 'success' }
                    response = web.Response(text=json.dumps(statusResult), status=201)
                except asyncpg.exceptions.UniqueViolationError as e:
                    statusResult = { 'Status' : e.detail }
                    response = web.Response(text=json.dumps(statusResult), status=409)
                return response
    else:
        response = status(500)
    return response

@routes.get('/get')
@routes.get('/get/{cpf}')
async def getUser_handler(request):
    """Recebe o request, se nao enviado nada, retorna tudo ou se tiver um cpf o cadastro do mesmo"""
    pool = request.app['pool']
    async with pool.acquire() as connection:
        userInfo = {}
        async with connection.transaction():
            r = redis.Redis(host="redis")

            if 'cpf' in request.match_info:
                existCPF = r.get(request.match_info['cpf'])
                if existCPF is not None:
                    userInfo = eval(existCPF)
                else:
                    results = await connection.fetch('select id,name,lastname,cpf,bday from users\
                        where cpf = \'{}\''.format(request.match_info['cpf']))
                    userInfo = dict(results[0])
                    r.setex(
                        str(userInfo['cpf']),
                        30,
                        value=str(userInfo)
                    )
                    userInfoCache = r.get(str(userInfo['cpf'])).decode("utf-8")
                    userInfoCache = eval(userInfoCache)
            else:
                # Run the query passing the request argument.
                results = await connection.fetch('select id,name,lastname,cpf,bday from users')
                for result in results:
                    userInfo[result['id']] = dict(result)
            status = { 'Result' : userInfo }
            response = web.Response(text=json.dumps(status), status=200)
            return response

async def main():
    """Inicia o server"""
    app = web.Application()
    app['pool'] = await asyncpg.create_pool(database='stone',
            user='userstone',password='gp3bHVe3', host='postgres')
    app.add_routes(routes)
    app.make_handler(keepalive_timeout=3)
    return app

loop = asyncio.get_event_loop()
app = loop.run_until_complete(main())
web.run_app(app)
