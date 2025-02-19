from odmantic import Model, Reference, EmbeddedModel
from typing import Optional
import datetime

class Perfil(Model):
    nome : Optional[str]
    email : str
    bio : str

class Album(EmbeddedModel):  # Álbum agora é um subdocumento
    titulo: str
    capa: str
    perfil: Perfil = Reference()


class Publicacoes(Model):
    legenda : str
    curtidas: int
    data_cricao: datetime.datetime
    imagem : str
    perfil: Perfil = Reference()
    album: list[Optional[Album]] = []



