from pydantic import BaseModel

class Server:
    pass

# Python >= 3.10
# class User(BaseModel):
#     username: str
#     password: str | None = None
#     comments: str | None = None
#     groups: list | None = None
#     home: bool | None = False
#     shell: str | None = "/bin/bash"

##Python <= 3.10
class User(BaseModel):
    username: str
    password: str = None
    comments: str = None
    groups: list = None
    home: bool = False
    shell: str = "/bin/bash"
