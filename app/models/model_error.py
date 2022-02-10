from typing import Any, Optional
from pydantic import BaseModel


class Error(BaseModel):
    code: Optional[str] = '0'
    message: Optional[str]
