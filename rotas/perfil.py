from fastapi import APIRouter, HTTPException
from database import get_engine
from models import Perfil
from odmantic import ObjectId

router = APIRouter(
    prefix="/perfil",
    tags=["perfil"],

)


engine = get_engine()


@router.get("/perfil", response_model=list[Perfil])
async def pegar_todos_perfis(skip: int = 0, limit: int = 10):
    perfis = await engine.find(Perfil, skip=skip, limit=limit)
    return perfis
        

@router.post("/perfil", response_model=Perfil)
async def criar_perfil(perfil : Perfil) -> Perfil:
    await engine.save(perfil)
    return perfil