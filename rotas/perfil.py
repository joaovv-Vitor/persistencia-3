import re

from fastapi import APIRouter, HTTPException, Query
from odmantic import ObjectId

from database import get_engine
from models import Perfil, Album, Publicacao

router = APIRouter(
    prefix="/perfil",
    tags=["perfil"],

)
engine = get_engine()


@router.get("/perfil", response_model=list[Perfil])  # Rota para pegar todos os perfis
async def pegar_todos_perfis(skip: int = 0, limit: int = 10):
    perfis = await engine.find(Perfil, skip=skip, limit=limit)
    return perfis


@router.post("/perfil", response_model=Perfil)  # Rota para criar um perfil
async def criar_perfil(perfil: Perfil) -> Perfil:
    await engine.save(perfil)
    return perfil


@router.get("/perfil/{perfil_id}", response_model=Perfil)  # Rota para pegar um perfil específico
async def pegar_perfil(perfil_id: str) -> Perfil:
    perfil = await engine.find_one(Perfil, Perfil.id == ObjectId(perfil_id))
    if perfil:
        return perfil
    raise HTTPException(status_code=404, detail="Perfil não encontrado")


@router.put("/perfil/{perfil_id}", response_model=Perfil)  # Rota para atualizar um perfil
async def atualizar_perfil(perfil_id: str, perfil: Perfil) -> Perfil:
    perfil = await engine.find_one(Perfil, Perfil.id == ObjectId(perfil_id))
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")

    updated_perfil = perfil.model_copy(update=perfil.model_dump(exclude_unset=True))

    await engine.save(updated_perfil)
    return updated_perfil


@router.delete("/perfil/{perfil_id}")  # Rota para deletar um perfil
async def deletar_perfil(perfil_id: str):
    perfil = await engine.find_one(Perfil, Perfil.id == ObjectId(perfil_id))
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
    await engine.delete(perfil)
    return {"message": "Perfil deletado com sucesso!"}


# Busca parcial por nome
@router.get("/buscar_parcial", response_model=list[Perfil])
async def buscar_perfil_por_nome(query: str = Query(..., description="Nome parcial do perfil para busca")):
    busc = re.compile(query, re.IGNORECASE)
    perfis = await engine.find(Perfil, Perfil.nome.match(busc))
    return perfis


# Contar número total de perfis
@router.get("/contagem")
async def contar_perfis():
    total = await engine.count(Perfil)
    return {"total_perfis": total}



#pegar todos os albuns e publicacoes de um perfil
@router.get("/perfil/{perfil_id}/albunsPerfil")
async def pegar_albuns_e_publicacoes_de_perfil(perfil_id: str):
    perfil = await engine.find_one(Perfil, Perfil.id == ObjectId(perfil_id))
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")

    albuns = await engine.find(Album, query.eq(Album.perfil, perfil.id))
    publicacao = await engine.find(Publicacao, query.eq(Publicacao.perfil, perfil.id))

    return {"perfil": perfil, "albuns": albuns, "publicacoes": publicacao}