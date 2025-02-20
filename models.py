from odmantic import Model, Reference, Field
from typing import Optional
import datetime

class Perfil(Model):
    nome : Optional[str]
    email : Optional[str]
    bio : Optional[str]


# Classe Publicacao
class Publicacao(Model):
    legenda: str
    curtidas: int
    data_criacao: datetime.datetime
    imagem: str
    perfil: Perfil = Reference()
    album_ids: list[str] = Field(default_factory=list)  # Lista de IDs de álbuns

# Classe Album
class Album(Model):
    titulo: str
    capa: str
    perfil: Perfil = Reference()
    publicacao_ids: Optional[list[str]] = Field(default_factory=list)  # Lista de IDs de publicações
    


# # Modelo Publicacoes
# class Publicacoes(Model):
#     legenda: str
#     curtidas: int
#     data_criacao: datetime
#     imagem: str
#     perfil: Perfil = Reference()  
#     album: Optional[list["Album"]] = []  

# # Modelo Album
# class Album(Model):
#     titulo: str
#     capa: str
#     perfil: Perfil = Reference()  
#     publicacoes: Optional[list[Publicacoes]] = []  