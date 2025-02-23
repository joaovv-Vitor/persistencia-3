import datetime
import re

from fastapi import APIRouter, HTTPException, Query
from odmantic import ObjectId

from database import get_engine
from models import Perfil, Publicacao

router = APIRouter(
    prefix="/publicacao",
    tags=["Publicacao"],

)

engine = get_engine()


@router.get("/publicacao", response_model=list[Publicacao])  # Rota para pegar todas as publicações
async def pegar_todas_publicacoes(skip: int = 0, limit: int = 10):
    publicacoes = await engine.find(Publicacao, skip=skip, limit=limit)
    return publicacoes


@router.post("/publicacao", response_model=Publicacao)  # Rota para criar uma publicação
async def criar_publicacao(publicacao: Publicacao) -> Publicacao:
    perfil = await engine.find_one(Perfil, Perfil.id == ObjectId(publicacao.perfil.id))
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
    publicacao.perfil = perfil
    await engine.save(publicacao)
    return publicacao


@router.get("/publicacao/{publicacao_id}", response_model=Publicacao)  # Rota para pegar uma publicação específica
async def pegar_publicacao(publicacao_id: str):
    publicacao = await engine.find_one(Publicacao, Publicacao.id == ObjectId(publicacao_id))
    if publicacao:
        return publicacao
    raise HTTPException(status_code=404, detail="Publicação não encontrada")


@router.put("/publicacao/{publicacao_id}", response_model=Publicacao)  # Rota para atualizar uma publicação
async def atualizar_publicacao(publicacao_id: str, publicacao_data: Publicacao) -> Publicacao:
    existing_publicacao = await engine.find_one(Publicacao, Publicacao.id == ObjectId(publicacao_id))
    if not existing_publicacao:
        raise HTTPException(status_code=404, detail="Publicação não encontrada")

    # Atualizando os campos da publicação existente com os novos dados
    updated_publicacao_data = publicacao_data.model_dump(exclude_unset=True)

    for key, value in updated_publicacao_data.items():
        setattr(existing_publicacao, key, value)

    await engine.save(existing_publicacao)
    return existing_publicacao


@router.delete("/publicacao/{publicacao_id}")  # Rota para deletar uma publicação
async def deletar_publicacao(publicacao_id: str):
    publicacao = await engine.find_one(Publicacao, Publicacao.id == ObjectId(publicacao_id))
    if not publicacao:
        raise HTTPException(status_code=404, detail="Publicação não encontrada")
    await engine.delete(publicacao)
    return {"message": "Publicação deletada com sucesso!"}


# Retorna as publicoes com base no id do perfil
@router.get("/publicacao/perfil/{perfil_id}", response_model=list[Publicacao])
async def get_publicacoes_por_perfil(perfil_id: str, skip: int = 0, limit: int = 10):
    # Compare o campo de referência diretamente com o ObjectId
    publicacoes = await engine.find(Publicacao, Publicacao.perfil == ObjectId(perfil_id), skip=skip, limit=limit)
    return publicacoes


# Retorna as publicaoces do album x
@router.get("/pub/album/{album_id}", response_model=list[Publicacao])
async def get_publicacoes_por_album(album_id: str, skip: int = 0, limit: int = 10):
    publicacoes = await engine.find(Publicacao, Publicacao.album_ids == album_id, skip=skip, limit=limit)
    return publicacoes


# Busca parcial na legenda
@router.get("/parcial", response_model=list[Publicacao])
async def parcial_publicacoes(query: str = Query(..., description="Texto:    "),
                             skip: int = 0, limit: int = 10):
    regex = re.compile(query, re.IGNORECASE)
    publicacoes = await engine.find(Publicacao, Publicacao.legenda.match(regex), skip=skip, limit=limit)
    return publicacoes


# Count total de publicações
@router.get("/countTotal")
async def total_publicacoes():
    pipeline = [
        {"$group": {"_id": None, "total": {"$sum": 1}}}
    ]
    collection = engine.get_collection(Publicacao)
    cursor = collection.aggregate(pipeline)
    resultado = await cursor.to_list(length=1)
    total = resultado[0]["total"] if resultado else 0
    return {"total_publicacoes": total}


# Busca as publicacoes com base no ano de postagem
@router.get("/ano/{year}", response_model=list[Publicacao])
async def get_pubs_por_ano(year: int, skip: int = 0, limit: int = 10):
    start_date = datetime.datetime(year, 1, 1)
    end_date = datetime.datetime(year, 12, 31, 23, 59, 59)

    publicacoes = await engine.find(
        Publicacao,
        (Publicacao.data_criacao >= start_date) & (Publicacao.data_criacao <= end_date),
        skip=skip,
        limit=limit
    )
    return publicacoes


# Ordena as pubs de um perfil com base nos likes(desc)
@router.get("/perfil/{perfil_id}/ordenado_manual", response_model=list[Publicacao])
async def get_pubs_ordenadas(perfil_id: str, skip: int = 0, limit: int = 10):
    try:
        perfil_id_obj = ObjectId(perfil_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de perfil inválido")

    pubs = await engine.find(Publicacao, Publicacao.perfil == perfil_id_obj)

    ordenadas = []

    while pubs:
        max_pub = max(pubs, key=lambda pub: pub.curtidas)
        ordenadas.append(max_pub)
        pubs.remove(max_pub)
    ordenadas = ordenadas[skip: skip + limit]

    return ordenadas
