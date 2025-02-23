from fastapi import FastAPI

from rotas import album, perfil, publi_album, publicacao

# FastAPI app instance
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(perfil.router)
app.include_router(album.router)
app.include_router(publicacao.router)
app.include_router(publi_album.router)
