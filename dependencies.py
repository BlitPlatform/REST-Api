from fastapi import Header, HTTPException


async def get_token_header(x_token: str = Header()):
    #will provide jwt auth in case is needed
    if x_token != "fake-jwt":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


#async def get_query_token(token: str):
#    if token != "fake-secret-token":
#        raise HTTPException(status_code=400, detail="No Jessica token provided")