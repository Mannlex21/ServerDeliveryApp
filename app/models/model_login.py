from pydantic import BaseModel


class Login(BaseModel):
    emailOrUser: str
    password: str
