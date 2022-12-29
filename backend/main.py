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


@app.post("/{hostname}/create_user/")
async def create_user(hostname, user: User):
    server = Unix(hostname=hostname,
                  credentials={"connection_type": "password", "username": "timba", "password": "mudar123",
                               "ssh_pass": None})
    user_dict = user.dict()
    print(user_dict)
    return {"detail": {
        "user": server.create_user(username=user_dict["username"], password=user_dict["password"],
                                   groups=user_dict["groups"],
                                   create_home=user_dict["home"], shell=user_dict["shell"])}}
