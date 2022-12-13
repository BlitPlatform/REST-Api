from pydantic import BaseModel

class Coordinates(BaseModel):
    x: str
    y: str
    z: str

class Port(BaseModel):
    start: Coordinates
    stop: Coordinates

