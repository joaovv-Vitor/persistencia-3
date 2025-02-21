from odmantic import Model, Reference, Field
import datetime

class Perfil(Model):
    nome: str | None = None
    email: str | None = None
    bio: str | None = None

# Classe Publicacao
class Publicacao(Model):
    legenda: str
    curtidas: int
    data_criacao: datetime.datetime
    imagem: str
    perfil: Perfil = Reference()
    album_ids: list[str] | None = Field(default_factory=list)

# Classe Album
class Album(Model):
    titulo: str | None = None
    capa: str | None = None
    perfil: Perfil = Reference()
    publicacao_ids: list[str] | None = Field(default_factory=list)
