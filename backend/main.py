from fastapi import FastAPI
from servers import Unix
from models import User

app = FastAPI()


@app.get("/")
async def root():
    return {"detail": "Boa sorte para usar! Feito com amor"}


@app.get("/{hostname}/users")
async def users(hostname):
    server = Unix(hostname=hostname,
                  credentials={"connection_type": "password", "username": "timba", "password": "mudar123",
                               "ssh_pass": None})
    return {"detail": {"users": server.get_users()}}


@app.get("/{hostname}/os")
async def users(hostname):
    server = Unix(hostname=hostname,
                  credentials={"connection_type": "password", "username": "timba", "password": "mudar123",
                               "ssh_pass": None})
    return {"detail": {"os": f"{server.get_os()}"}}


@app.get("/{hostname}/groups")
async def groups(hostname):
    server = Unix(hostname=hostname,
                  credentials={"connection_type": "password", "username": "timba", "password": "mudar123",
                               "ssh_pass": None})
    return {"detail": {"groups": server.get_groups()}}


@app.post("/{hostname}/user/create")
async def create_user(hostname, user: User):
    server = Unix(hostname=hostname,
                  credentials={"connection_type": "password", "username": "timba", "password": "mudar123",
                               "ssh_pass": None})
    user_dict = user.dict()
    return {"detail": server.create_user(username=user_dict["username"], password=user_dict["password"],
                                         groups=user_dict["groups"],
                                         create_home=user_dict["home"], shell=user_dict["shell"])}


@app.get("/{hostname}/user/unlock/{username}")
async def unlock_user(hostname, username):
    server = Unix(hostname=hostname,
                  credentials={"connection_type": "password", "username": "timba", "password": "mudar123",
                               "ssh_pass": None})
    return {"detail": server.unlock_user(user=username)}


@app.delete("/{hostname}/user/{user}")
async def delete_user(hostname, user):
    server = Unix(hostname=hostname,
                  credentials={"connection_type": "password", "username": "timba", "password": "mudar123",
                               "ssh_pass": None})
    return {"detail": server.delete_user(user)}
