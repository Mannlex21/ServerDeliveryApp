from pydantic import BaseModel


class Image(BaseModel):
    imageBase64: str
    type: str
    filename: str
