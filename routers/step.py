from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_token_header
from models.datamodel import Data
from services.common.decoders.b64helper import decode_from_b64

router = APIRouter(
    prefix="/step",
    tags=["step"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post("/upload")
async def handle_step(data: Data) -> None:
    if data.filename is None:
        raise HTTPException(
            status_code=422, detail="The filedata parameter is missing."
        )
    step = decode_from_b64(data.filedata)
    print(step)
