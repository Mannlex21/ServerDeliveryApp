from typing import Optional
from pydantic import BaseModel


class UserDetails(BaseModel):
    idUserDetail: Optional[int]
    idUser: Optional[int]
    firstName: str
    lastName: str
    areaCode: str
    phoneNumber: str
