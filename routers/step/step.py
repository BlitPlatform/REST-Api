from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import Response
from dependencies import get_token_header
from models.datamodel import Data
from services.common.decoders.b64helper import decode_from_b64
from services.step.stepservice import step2tsl
from services.common.diroperations.dirservice import remove_user_directory
import os

router = APIRouter(
    prefix="/step",
    tags=["step"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post("/upload")
async def handle_step(background_tasks: BackgroundTasks, data: Data) -> Response:
    if data.filename is None:
        raise HTTPException(
            status_code=422, detail="The filedata parameter is missing."
        )
    step = decode_from_b64(data.filedata)
    #print(step)
    zip_file = step2tsl(step)

    stream_value = zip_file['stream_value']
    zip_filename = zip_file['file_name']

    resp = Response(stream_value, media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename={zip_filename}'
    })

    background_tasks.add_task(remove_user_directory, os.getcwd())
    return resp
    
