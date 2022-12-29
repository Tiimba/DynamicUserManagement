from pydantic import BaseModel


class Server:
    pass


class User(BaseModel):
    username: str
    password: str | None = None
    groups: list | None = None
    home: bool | None = False
    shell: str | None = "/bin/bash"
