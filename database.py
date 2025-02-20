from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Busca a URL de conexão do MongoDB Atlas do arquivo .env
DATABASE_URL = os.getenv("DATABASE_URL")
# Valida se a URL foi carregada corretamente
if not DATABASE_URL:
    raise ValueError("A variável de ambiente DATABASE_URL não foi definida.")

# Cria o cliente do MongoDB usando motor
client = AsyncIOMotorClient(DATABASE_URL)

# Define o banco de dados a ser usado
db = client.mydatabase

# Cria uma instância do AIOEngine do odmantic
engine = AIOEngine(client=client, database="persistencia-3")

# Função para retornar a instância do AIOEngine
def get_engine() -> AIOEngine:
    return engine