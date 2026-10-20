import re
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pymongo import ReturnDocument
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.errors import DuplicateKeyError

from ..database import get_colecao_jogos
from ..schemas import (
    JogoCreate,
    JogoListResponse,
    JogoResponse,
    JogoUpdate,
    Plataforma,
)

router = APIRouter(prefix="/jogos", tags=["Jogos"])

Colecao = Annotated[AsyncCollection, Depends(get_colecao_jogos)]

MSG_NAO_ENCONTRADO = "Jogo não encontrado"
MSG_DUPLICADO = "Já existe um jogo com esse título nessa plataforma"


def _object_id(jogo_id: str) -> ObjectId:
    if not ObjectId.is_valid(jogo_id):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "ID inválido")
    return ObjectId(jogo_id)


# ---------- CREATE ----------
@router.post("", response_model=JogoResponse, status_code=status.HTTP_201_CREATED)
async def criar_jogo(jogo: JogoCreate, colecao: Colecao):
    documento = jogo.model_dump(mode="json")
    try:
        await colecao.insert_one(documento)  # adiciona "_id" ao dicionário
    except DuplicateKeyError:
        raise HTTPException(status.HTTP_409_CONFLICT, MSG_DUPLICADO)
    return documento


# ---------- READ (lista com filtros e paginação) ----------
@router.get("", response_model=JogoListResponse)
async def listar_jogos(
    colecao: Colecao,
    busca: str | None = Query(None, description="Busca parcial no título"),
    plataforma: Plataforma | None = None,
    genero: str | None = None,
    preco_min: float | None = Query(None, ge=0),
    preco_max: float | None = Query(None, ge=0),
    em_estoque: bool | None = Query(None, description="True = só jogos com estoque"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    filtro: dict = {}

    if busca:
        filtro["titulo"] = {"$regex": re.escape(busca), "$options": "i"}
    if plataforma:
        filtro["plataforma"] = plataforma.value
    if genero:
        filtro["genero"] = {"$regex": f"^{re.escape(genero)}$", "$options": "i"}
    if preco_min is not None or preco_max is not None:
        faixa = {}
        if preco_min is not None:
            faixa["$gte"] = preco_min
        if preco_max is not None:
            faixa["$lte"] = preco_max
        filtro["preco"] = faixa
    if em_estoque is not None:
        filtro["estoque"] = {"$gt": 0} if em_estoque else {"$eq": 0}

    total = await colecao.count_documents(filtro)
    cursor = colecao.find(filtro).sort("titulo", 1).skip(skip).limit(limit)
    itens = await cursor.to_list(length=limit)

    return {"total": total, "skip": skip, "limit": limit, "itens": itens}


# ---------- READ (um jogo) ----------
@router.get("/{jogo_id}", response_model=JogoResponse)
async def buscar_jogo(jogo_id: str, colecao: Colecao):
    jogo = await colecao.find_one({"_id": _object_id(jogo_id)})
    if jogo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, MSG_NAO_ENCONTRADO)
    return jogo


# ---------- UPDATE (substituição completa) ----------
@router.put("/{jogo_id}", response_model=JogoResponse)
async def substituir_jogo(jogo_id: str, jogo: JogoCreate, colecao: Colecao):
    try:
        atualizado = await colecao.find_one_and_replace(
            {"_id": _object_id(jogo_id)},
            jogo.model_dump(mode="json"),
            return_document=ReturnDocument.AFTER,
        )
    except DuplicateKeyError:
        raise HTTPException(status.HTTP_409_CONFLICT, MSG_DUPLICADO)
    if atualizado is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, MSG_NAO_ENCONTRADO)
    return atualizado


# ---------- UPDATE (parcial) ----------
@router.patch("/{jogo_id}", response_model=JogoResponse)
async def atualizar_jogo(jogo_id: str, dados: JogoUpdate, colecao: Colecao):
    # Campos omitidos ou enviados como null são ignorados.
    campos = dados.model_dump(mode="json", exclude_unset=True, exclude_none=True)
    if not campos:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Nenhum campo para atualizar")

    try:
        atualizado = await colecao.find_one_and_update(
            {"_id": _object_id(jogo_id)},
            {"$set": campos},
            return_document=ReturnDocument.AFTER,
        )
    except DuplicateKeyError:
        raise HTTPException(status.HTTP_409_CONFLICT, MSG_DUPLICADO)
    if atualizado is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, MSG_NAO_ENCONTRADO)
    return atualizado


# ---------- DELETE ----------
@router.delete("/{jogo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_jogo(jogo_id: str, colecao: Colecao):
    resultado = await colecao.delete_one({"_id": _object_id(jogo_id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND, MSG_NAO_ENCONTRADO)
