import os
from fastapi import FastAPI, Depends
from app import user, shop, client, client_store, dependencies, admin
app = FastAPI(dependencies=[Depends(dependencies.get_query_token)])


app = FastAPI()
app.include_router(user.router)
app.include_router(shop.router)
app.include_router(client.router)
app.include_router(client_store.router)
app.include_router(
    admin.router,
    prefix="/admin",
    # tags=["admin"],
    # dependencies=[Depends(dependencies.get_token_header)],
    # responses={418: {"description": "I'm a teapot"}},
)
