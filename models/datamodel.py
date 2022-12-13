from pydantic import BaseModel
from models.filemodel import FileData

class StepData(BaseModel):
    file: FileData
