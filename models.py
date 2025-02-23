import datetime
from typing import Optional

from odmantic import Field, Model, Reference


class Perfil(Model):
    nome: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None


# Classe Publicacao
class Publicacao(Model):
    legenda: str
    curtidas: int
    data_criacao: datetime.datetime
    imagem: str
    perfil: Perfil = Reference()
    album_ids: Optional[list[str]] = Field(default_factory=list)


# Classe Album
class Album(Model):
    titulo: Optional[str] = None
    capa: Optional[str] = None
    perfil: Perfil = Reference()
    publicacao_ids: Optional[list[str]] = Field(default_factory=list)
