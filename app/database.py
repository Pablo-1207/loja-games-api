from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection

from .config import settings

# O cliente conecta de forma preguiçosa: nada acontece até a primeira operação.
client: AsyncMongoClient = AsyncMongoClient(settings.mongo_url)
db = client[settings.mongo_db]


def get_colecao_jogos() -> AsyncCollection:
    """Dependência do FastAPI que entrega a coleção de jogos."""
    return db["jogos"]
