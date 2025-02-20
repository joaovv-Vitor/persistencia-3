from fastapi import FastAPI
from rotas import perfil, album, publicacao, publi_album

# FastAPI app instance
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}



app.include_router(perfil.router)
app.include_router(album.router)
app.include_router(publicacao.router)
app.include_router(publi_album.router)  
