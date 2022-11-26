from fastapi import Depends, FastAPI

from dependencies import get_token_header
from routers import step, stl

#app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

app.include_router(step.router)
app.include_router(stl.router)


@app.get("/")
async def root():
    return {"message": "Welcome to BlitAI Api"}