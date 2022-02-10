from typing import Optional
import bcrypt
from pydantic import BaseModel

from app.models.model_user_details import UserDetails


class User(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: Optional[str]
    key: Optional[str]
    details: Optional[UserDetails]

    @classmethod
    async def get_user(cls, username):
        return cls.get_user(username=username)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)
