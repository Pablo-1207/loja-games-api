from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import client, db
from .routers import jogos


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Impede o mesmo título de ser cadastrado duas vezes na mesma plataforma.
    await db["jogos"].create_index(
        [("titulo", 1), ("plataforma", 1)], unique=True, name="uq_titulo_plataforma"
    )
    yield
    await client.close()


app = FastAPI(
    title="Loja de Games API",
    description="CRUD de jogos com FastAPI e MongoDB.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(jogos.router)


@app.get("/", tags=["Status"])
async def raiz():
    return {"status": "ok", "docs": "/docs"}
