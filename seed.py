"""Insere dados de exemplo na coleção jogos usando Python + PyMongo.

Execute com o MongoDB ligado:
    python seed.py
"""
from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017"
BANCO = "loja_games"

JOGOS = [
    {
        "titulo": "Elden Ring",
        "descricao": "RPG de ação em mundo aberto.",
        "plataforma": "PlayStation 5",
        "genero": "RPG",
        "preco": 249.90,
        "estoque": 15,
        "desenvolvedora": "FromSoftware",
        "classificacao_etaria": 16,
        "data_lancamento": "2022-02-25",
    },
    {
        "titulo": "The Legend of Zelda: Tears of the Kingdom",
        "plataforma": "Nintendo Switch",
        "genero": "Aventura",
        "preco": 349.90,
        "estoque": 8,
        "desenvolvedora": "Nintendo",
        "classificacao_etaria": 12,
        "data_lancamento": "2023-05-12",
    },
    {
        "titulo": "Hollow Knight",
        "plataforma": "PC",
        "genero": "Metroidvania",
        "preco": 46.99,
        "estoque": 0,
        "desenvolvedora": "Team Cherry",
        "classificacao_etaria": 10,
        "data_lancamento": "2017-02-24",
    },
    {
        "titulo": "Forza Horizon 5",
        "plataforma": "Xbox Series X|S",
        "genero": "Corrida",
        "preco": 199.90,
        "estoque": 5,
        "desenvolvedora": "Playground Games",
        "classificacao_etaria": 0,
        "data_lancamento": "2021-11-09",
    },
]


def main():
    with MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000) as cliente:
        cliente.admin.command("ping")
        colecao = cliente[BANCO]["jogos"]
        for jogo in JOGOS:
            resultado = colecao.update_one(
                {"titulo": jogo["titulo"], "plataforma": jogo["plataforma"]},
                {"$setOnInsert": jogo},
                upsert=True,
            )
            acao = "inserido" if resultado.upserted_id else "já existia"
            print(f"{jogo['titulo']}: {acao}")
        print(f"\nTotal de jogos na coleção: {colecao.count_documents({})}")


if __name__ == "__main__":
    main()
