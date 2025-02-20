from fastapi import FastAPI
from rotas import perfil, album

# FastAPI app instance
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}



app.include_router(perfil.router)
app.include_router(album.router)