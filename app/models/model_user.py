import bcrypt
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

    @classmethod
    async def get_user(cls, username):
        return cls.get_user(username=username)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)
