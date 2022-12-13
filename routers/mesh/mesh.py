from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import Response
from dependencies import get_token_header
from models.meshmodel import MeshData
from services.common.decoders.b64helper import decode_from_b64
from services.mesh.meshservice import generate_mesh

router = APIRouter(
    prefix="/mesh",
    tags=["mesh"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/generateMesh")
async def handle_step(background_tasks: BackgroundTasks, data: MeshData) -> Response:
    files = data.stl_files
    mesh_options = {
        "min_frequency": data.min_frequency,
        "max_frequency": data.max_frequency,
        "source_port": data.source_port,
        "perfectly_matcher_layer": data.perfectly_matched_layer,
        "factor": data.factor,
        "factor_space": data.factor_space,
        "fraction": data.fraction,
        "number_of_cells": data.number_of_cells
    }
    if files is None:
        raise HTTPException(
            status_code=422, detail="The step file parameter is missing."
        )

    #stl_files = [decode_from_b64(file.filedata) for file in files]
    
    generate_mesh(files, mesh_options)



    #resp = Response(
    #    stream_value,
    #    media_type="application/x-zip-compressed",
    #    headers={"Content-Disposition": f"attachment;filename={zip_filename}"},
    #)

    return {"message": "Parsed everything succesfully"}

    #background_tasks.add_task(remove_user_directory, os.getcwd())
    #return resp
