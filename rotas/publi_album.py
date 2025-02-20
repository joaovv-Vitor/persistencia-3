from fastapi import APIRouter, HTTPException
from database import get_engine
from models import Perfil, Publicacao, Album
from odmantic import ObjectId

router = APIRouter(
    prefix="/publi_album",
    tags=["Publi_album"],

)

engine = get_engine()

@router.post("/publi_album") # Rota para associar uma publicação a um álbum
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

@router.delete("/publi_album") # Rota para desassociar uma publicação de um álbum
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


    