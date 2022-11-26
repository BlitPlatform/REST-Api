from pydantic import BaseModel


class Data(BaseModel):
    filename: str
    filedata: str
