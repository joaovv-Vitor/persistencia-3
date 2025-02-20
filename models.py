from odmantic import Model, Reference, EmbeddedModel
from typing import Optional
import datetime

class Perfil(Model):
    nome : Optional[str]
    email : str
    bio : str


# Modelo Publicacoes
class Publicacoes(Model):
    legenda: str
    curtidas: int
    data_criacao: datetime
    imagem: str
    perfil: Perfil = Reference()  
    album: Optional[list["Album"]] = []  

# Modelo Album
class Album(Model):
    titulo: str
    capa: str
    perfil: Perfil = Reference()  
    publicacoes: Optional[list[Publicacoes]] = []  
    

    


