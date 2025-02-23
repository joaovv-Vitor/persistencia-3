from fastapi import APIRouter, HTTPException
from odmantic import ObjectId

from database import get_engine
from models import Album, Publicacao

router = APIRouter(
    prefix="/publi_album",
    tags=["Publi_album"],

)

engine = get_engine()


@router.post("/publi_album")  # Rota para associar uma publicação a um álbum
async def associar_publi_album(publi_id: str, album_id: str):
    publi = await engine.find_one(Publicacao, Publicacao.id == ObjectId(publi_id))
    if not publi:
        raise HTTPException(status_code=404, detail="Publicação não encontrada")

    album = await engine.find_one(Album, Album.id == ObjectId(album_id))
    if not album:
        raise HTTPException(status_code=404, detail="Álbum não encontrado")

    # up_publi = publi.model_copy(update={"album_ids": [ObjectId(album_id)]})
    # await engine.save(up_publi)

    publi.album_ids.append(str(album_id))
    await engine.save(publi)

    album.publicacao_ids.append(str(publi_id))
    await engine.save(album)

    return {"message": 'album e publicação associados com sucesso!'}


@router.delete("/publi_album")  # Rota para desassociar uma publicação de um álbum
async def desassociar_publi_album(publi_id: str, album_id: str):
    publi = await engine.find_one(Publicacao, Publicacao.id == ObjectId(publi_id))
    if not publi:
        raise HTTPException(status_code=404, detail="Publicação não encontrada")

    album = await engine.find_one(Album, Album.id == ObjectId(album_id))
    if not album:
        raise HTTPException(status_code=404, detail="Álbum não encontrado")

    publi.album_ids.remove(str(album_id))
    await engine.save(publi)

    album.publicacao_ids.remove(str(publi_id))
    await engine.save(album)

    return {"message": 'album e publicação desassociados com sucesso!'}


@router.put("/publi_album")
async def atualizar_associacao_publi_album(publi_id: str, old_album_id: str, new_album_id: str):

    publi = await engine.find_one(Publicacao, Publicacao.id == ObjectId(publi_id))
    if not publi:
        raise HTTPException(status_code=404, detail="Publicação não encontrada")

    old_album = await engine.find_one(Album, Album.id == ObjectId(old_album_id))
    if not old_album:
        raise HTTPException(status_code=404, detail="Álbum antigo não encontrado")

    new_album = await engine.find_one(Album, Album.id == ObjectId(new_album_id))
    if not new_album:
        raise HTTPException(status_code=404, detail="Novo álbum não encontrado")

    if str(old_album_id) not in publi.album_ids:
        raise HTTPException(status_code=400, detail="Publicação não associada ao álbum antigo especificado")

    # Remove o álbum antigo e adiciona o novo, se ainda não estiver associado
    publi.album_ids.remove(str(old_album_id))
    if str(new_album_id) not in publi.album_ids:
        publi.album_ids.append(str(new_album_id))
    await engine.save(publi)

    # Atualiza o álbum antigo: remove a publicação da lista
    if str(publi_id) in old_album.publicacao_ids:
        old_album.publicacao_ids.remove(str(publi_id))
        await engine.save(old_album)

    # Atualiza o novo álbum: adiciona a publicação, se ainda não estiver associada
    if str(publi_id) not in new_album.publicacao_ids:
        new_album.publicacao_ids.append(str(publi_id))
        await engine.save(new_album)

    return {"message": "Associação atualizada com sucesso!"}
