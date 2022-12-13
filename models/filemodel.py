from pydantic import BaseModel


class FileData(BaseModel):
    filename: str
    filedata: str
