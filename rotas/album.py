from fastapi import APIRouter, HTTPException
from database import get_engine
from models import Perfil, Publicacao, Album
from odmantic import ObjectId

router = APIRouter(
    prefix="/album",
    tags=["Album"],

)
engine = get_engine()



# @router.get("/album", response_model=list[Album]) # Rota para pegar todos os álbuns
# async def pegar_todos_albums(skip: int = 0, limit: int = 10):
#     albums = await engine.find(Album, skip=skip, limit=limit)
#     return albums

@router.get("/album", response_model=list[Album]) # Rota para pegar todos os álbuns
async def pegar_todos_albums(skip: int = 0, limit: int = 10):
    albums = await engine.find(Album, skip=skip, limit=limit)
    return albums


@router.get("/album/{album_id}", response_model=Album) # Rota para pegar um álbum específico
async def pegar_album(album_id: str):
    album = await engine.find_one(Album, Album.id == ObjectId(album_id))
    if album:
        return album
    raise HTTPException(status_code=404, detail="Album não encontrado")


#atualizar
@router.post("/album", response_model=Album) # Rota para criar um álbum
async def criar_album(album: Album) -> Album:
    perfil = await engine.find_one(Perfil, Perfil.id == ObjectId(album.perfil.id))
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
    album.perfil = perfil
    await engine.save(album)
    return album

@router.put("/album/{album_id}", response_model=Album) # Rota para atualizar um álbum
async def atualizar_album(album_id: str, album: Album) -> Album:
    existing_album = await engine.find_one(Album, Album.id == ObjectId(album_id))
    if not existing_album:
        raise HTTPException(status_code=404, detail="Album não encontrado")
    
    updated_album = album.model_copy(update={"id": ObjectId(album_id)})
    await engine.save(updated_album)
    return updated_album
