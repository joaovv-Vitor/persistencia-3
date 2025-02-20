from fastapi import APIRouter, HTTPException
from database import get_engine
from models import Perfil, Publicacao, Album
from odmantic import ObjectId

router = APIRouter(
    prefix="/publicacao",
    tags=["Publicacao"],

)

engine = get_engine()

@router.get("/publicacao", response_model=list[Publicacao]) # Rota para pegar todas as publicações
async def pegar_todas_publicacoes(skip: int = 0, limit: int = 10):
    publicacoes = await engine.find(Publicacao, skip=skip, limit=limit)
    return publicacoes

@router.post("/publicacao", response_model=Publicacao) # Rota para criar uma publicação
async def criar_publicacao(publicacao: Publicacao) -> Publicacao:
    perfil = await engine.find_one(Perfil, Perfil.id == ObjectId(publicacao.perfil.id))
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
    publicacao.perfil = perfil
    await engine.save(publicacao)
    return publicacao
