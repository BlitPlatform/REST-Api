from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dependencies import get_token_header
from routers.stl import stl
from routers.step import step
from logging.config import dictConfig
import logging
from properties.log_properties import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("blit")


#app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(step.router)
app.include_router(stl.router)


@app.get("/")
async def root():
    logger.debug("Starting UP API")
    return {"message": "Welcome to BlitAI Api"}