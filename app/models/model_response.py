from typing import Any, List, Optional
from pydantic import BaseModel
from app.models.model_error import Error


class Response(BaseModel):
    success: Optional[bool]
    failure: Optional[bool]
    value: Optional[Any]
    errorList: Optional[List[Error]]

    def create(value: Any = None):
        return Response(success=True, failure=False, value=value)

    def createError(errorList: Any, value: Any = None):
        return Response(success=False, failure=True, value=value, errorList=errorList)
