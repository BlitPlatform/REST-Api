from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from dependencies import get_token_header
from models.datamodel import Data
from services.common.decoders.b64helper import decode_from_b64
from services.step.stepservice import step2tsl

router = APIRouter(
    prefix="/step",
    tags=["step"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post("/upload")
async def handle_step(data: Data) -> FileResponse:
    if data.filename is None:
        raise HTTPException(
            status_code=422, detail="The filedata parameter is missing."
        )
    step = decode_from_b64(data.filedata)
    #print(step)
    entities = step2tsl(step)
    #return FileResponse()
    return entities
    
