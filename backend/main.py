from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from servers import Unix
from models import User
import configparser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

credentials = {
    "connection_type": "password",
    "username": "timba",
    "password": "mudar123",
    "ssh_pass": None
}

def get_unix_server(hostname):
    return Unix(hostname=hostname, credentials=credentials)

@app.get("/")
async def root():
    """
    Página inicial da API
    """
    return {"detail": "Boa sorte para usar! Feito com amor"}


@app.get("/{hostname}/users")
async def users(hostname):
    """
    Obtém todos os usuários do servidor Unix
    """
    server = get_unix_server(hostname)
    return {"detail": server.get_users()}

@app.get("/{hostname}/users/{username}/")
async def user(hostname, username):
    ''' Get specificied user '''

    server = get_unix_server(hostname)
    return {"deatil": server.get_user(username)}


@app.get("/{hostname}/os")
async def os(hostname):
    """
    Obtém o sistema operacional do servidor Unix
    """
    server = get_unix_server(hostname)
    return {"detail": {"os": f"{server.get_os()}"}}


@app.get("/{hostname}/groups")
async def groups(hostname):
    server = get_unix_server(hostname)
    return {"detail": {"groups": server.get_groups()}}


@app.post("/{hostname}/user/create")
async def create_user(hostname, user: User):
    server = get_unix_server(hostname)
    user_dict = user.dict()
    return {"detail": server.create_user(username=user_dict["username"], password=user_dict["password"],
                                         groups=user_dict["groups"],
                                         comments=user_dict["comments"],
                                         create_home=user_dict["home"], shell=user_dict["shell"])}

@app.get("/{hostname}/user/unlock/{username}")
async def unlock_user(hostname, username):
    server = get_unix_server(hostname)
    return {"detail": server.unlock_user(user=username)}


@app.get("/{hostname}/user/lock/{username}")
async def unlock_user(hostname, username):
    server = get_unix_server(hostname)
    return {"detail": server.lock_user(user=username)}


@app.delete("/{hostname}/user/{user}")
async def delete_user(hostname, user):
    server = get_unix_server(hostname)
    return {"detail": server.delete_user(user)}
