from typing import Optional
from pydantic import BaseModel


class Store(BaseModel):
    id: Optional[int]
    name: str
    description: str
    image: Optional[str]
