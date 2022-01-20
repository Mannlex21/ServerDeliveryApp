from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    user: str
    password: str
    email: str