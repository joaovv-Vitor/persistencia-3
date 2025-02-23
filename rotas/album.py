import re

from fastapi import APIRouter, HTTPException, Query
from odmantic import ObjectId, query

from database import get_engine
from models import Album, Perfil, Publicacao

router = APIRouter(
    prefix="/album",
    tags=["Album"],

)
engine = get_engine()


@router.get("/album", response_model=list[Album])  # Rota para pegar todos os álbuns
async def pegar_todos_albums(skip: int = 0, limit: int = 10):
    albums = await engine.find(Album, skip=skip, limit=limit)
    return albums


@router.get("/album/{album_id}", response_model=Album)  # Rota para pegar um álbum específico
async def pegar_album(album_id: str):
    album = await engine.find_one(Album, Album.id == ObjectId(album_id))
    if album:
        return album
    raise HTTPException(status_code=404, detail="Album não encontrado")


# atualizar
@router.post("/album", response_model=Album)  # Rota para criar um álbum
async def criar_album(album: Album) -> Album:
    perfil = await engine.find_one(Perfil, Perfil.id == ObjectId(album.perfil.id))
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
    album.perfil = perfil
    uptade_album = album.model_copy(update={"id": ObjectId(album.id)})
    await engine.save(uptade_album)
    return uptade_album


@router.put("/album/{album_id}", response_model=Album)  # Rota para atualizar um álbum
async def atualizar_album(album_id: str, album_data: Album) -> Album:
    existing_album = await engine.find_one(Album, Album.id == ObjectId(album_id))
    if not existing_album:
        raise HTTPException(status_code=404, detail="Album não encontrado")

    # Atualizando os campos do álbum existente com os novos dados
    updated_album_data = album_data.model_dump(exclude_unset=True)

    for key, value in updated_album_data.items():
        setattr(existing_album, key, value)

    await engine.save(existing_album)
    return existing_album


@router.delete("/album/{album_id}")  # Rota para deletar um álbum
async def deletar_album(album_id: str):
    album = await engine.find_one(Album, Album.id == ObjectId(album_id))
    if not album:
        raise HTTPException(status_code=404, detail="Album não encontrado")
    await engine.delete(album)
    return {"message": "Album deletado com sucesso!"}


# Pegar todas as publicações de um album
@router.get("/album/{album_id}/publicacoes", response_model=list[Publicacao])
async def pegar_publicacoes_album(album_id: str):
    album = await engine.find_one(Album, Album.id == ObjectId(album_id))
    if not album:
        raise HTTPException(status_code=404, detail="Album não encontrado")

    # Convertendo publicacao_ids para ObjectId
    publicacao_ids = [ObjectId(pub_id) for pub_id in album.publicacao_ids if ObjectId.is_valid(pub_id)]

    publicacoes = await engine.find(Publicacao, query.in_(Publicacao.id, publicacao_ids))
    return publicacoes


# Retorna os albuns do perfil x
@router.get("/perfil/{perfil_id}", response_model=list[Album])
async def get_albuns_por_perfil(perfil_id: str, skip: int = 0, limit: int = 10):
    # Checa se perfil existe
    perfil_obj = await engine.find_one(Perfil, Perfil.id == ObjectId(perfil_id))
    if not perfil_obj:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")

    # procura os albuns do perfil encontrado
    albuns = await engine.find(Album, Album.perfil == perfil_obj.id, skip=skip, limit=limit)
    return albuns


# Busca parcial nos titulos dos albuns
@router.get("/search", response_model=list[Album])
async def search_album_por_titulo(query: str = Query(..., description="Texto parcial para busca no título"),
                                  skip: int = 0, limit: int = 10):
    regex = re.compile(query, re.IGNORECASE)
    albuns = await engine.find(Album, Album.titulo.match(regex), skip=skip, limit=limit)
    return albuns


# Busca as publicacoes do album x
@router.get("/album/{album_id}/publicacoes", response_model=list[Publicacao])
async def get_publicacoes_album(album_id: str, skip: int = 0, limit: int = 10):
    album = await engine.find_one(Album, Album.id == ObjectId(album_id))
    if not album:
        raise HTTPException(status_code=404, detail="Album não encontrado")

    publicacao_ids = [ObjectId(pub_id) for pub_id in album.publicacao_ids if ObjectId.is_valid(pub_id)]
    publicacoes = await engine.find(Publicacao, query.in_(Publicacao.id, publicacao_ids), skip=skip, limit=limit)
    return publicacoes
