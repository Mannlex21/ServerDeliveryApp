from pydantic import BaseModel


class User(BaseModel):
    id: int
    user: str
    password: str
    email: str
