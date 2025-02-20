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

@router.get("/publicacao/{publicacao_id}", response_model=Publicacao) # Rota para pegar uma publicação específica
async def pegar_publicacao(publicacao_id: str):
    publicacao = await engine.find_one(Publicacao, Publicacao.id == ObjectId(publicacao_id))
    if publicacao:
        return publicacao
    raise HTTPException(status_code=404, detail="Publicação não encontrada")


# @router.put("/album/{album_id}", response_model=Album) # Rota para atualizar um álbum
# async def atualizar_album(album_id: str, album_data: Album) -> Album:
#     existing_album = await engine.find_one(Album, Album.id == ObjectId(album_id))
#     if not existing_album:
#         raise HTTPException(status_code=404, detail="Album não encontrado")
    
#     # Atualizando os campos do álbum existente com os novos dados
#     updated_album_data = album_data.model_dump(exclude_unset=True)
    
#     for key, value in updated_album_data.items():
#         setattr(existing_album, key, value)
    
#     await engine.save(existing_album)
#     return existing_album


@router.put("/publicacao/{publicacao_id}", response_model=Publicacao) # Rota para atualizar uma publicação
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


@router.delete("/publicacao/{publicacao_id}") # Rota para deletar uma publicação
async def deletar_publicacao(publicacao_id: str):
    publicacao = await engine.find_one(Publicacao, Publicacao.id == ObjectId(publicacao_id))
    if not publicacao:
        raise HTTPException(status_code=404, detail="Publicação não encontrada")
    await engine.delete(publicacao)
    return {"message": "Publicação deletada com sucesso!"}