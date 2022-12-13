from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_token_header
from models.datamodel import StepData
from services.common.decoders.b64helper import decode_from_b64

router = APIRouter(
    prefix="/stl",
    tags=["stl"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post("/upload")
async def handle_step(data: StepData) -> None:
    if data.filename is None:
        raise HTTPException(
            status_code=422, detail="The filedata parameter is missing."
        )
    step = decode_from_b64(data.filedata)
    print(step)
