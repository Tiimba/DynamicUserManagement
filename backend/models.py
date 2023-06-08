import platform
from pydantic import BaseModel
python_version = tuple(map(int, platform.python_version_tuple()))

class Server:
    pass


class User(BaseModel):
    username: str
    password: str = None
    comments: str = None
    groups: list = None
    home: bool = False
    shell: str = "/bin/bash"

if python_version >= (3, 10):
    User.__annotations__["password"] = str | None
    User.__annotations__["comments"] = str | None
    User.__annotations__["groups"] = list | None
    User.__annotations__["home"] = bool | None
    User.__annotations__["shell"] = str | None