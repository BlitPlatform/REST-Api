from pydantic import BaseModel
from typing import List, Optional
from models.filemodel import FileData
from models.portmodel import Port
from models.portmodel import Coordinates

class MeshData(BaseModel):
    stl_files: List[FileData] = []
    min_frequency: str
    max_frequency: str
    source_port: Port
    perfectly_matched_layer: str
    factor: str
    factor_space: str
    fraction: str
    number_of_cells: Coordinates
