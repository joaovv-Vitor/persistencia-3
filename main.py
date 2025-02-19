from fastapi import FastAPI
from rotas import perfil

# FastAPI app instance
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}



app.include_router(perfil.router)