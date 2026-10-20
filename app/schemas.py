from datetime import date
from enum import Enum
from typing import Annotated, Literal

from pydantic import AliasChoices, BaseModel, BeforeValidator, ConfigDict, Field

# Converte o ObjectId do Mongo para str automaticamente.
ObjectIdStr = Annotated[str, BeforeValidator(str)]


ClassificacaoEtaria = Literal[0, 10, 12, 14, 16, 18]


class Plataforma(str, Enum):
    PC = "PC"
    PS4 = "PlayStation 4"
    PS5 = "PlayStation 5"
    XBOX_ONE = "Xbox One"
    XBOX_SERIES = "Xbox Series X|S"
    SWITCH = "Nintendo Switch"


class JogoBase(BaseModel):
    titulo: str = Field(min_length=1, max_length=150, examples=["The Legend of Zelda: Tears of the Kingdom"])
    descricao: str | None = Field(default=None, max_length=2000)
    plataforma: Plataforma
    genero: str = Field(min_length=1, max_length=50, examples=["Aventura"])
    preco: float = Field(gt=0, examples=[349.90])
    estoque: int = Field(default=0, ge=0)
    desenvolvedora: str | None = Field(default=None, max_length=100)
    classificacao_etaria: ClassificacaoEtaria | None = Field(
        default=None, description="Classificação indicativa (Livre = 0)."
    )
    data_lancamento: date | None = None


class JogoCreate(JogoBase):
    pass


class JogoUpdate(BaseModel):
    """Todos os campos são opcionais — usado no PATCH."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"preco": 299.90},
                {"preco": 299.90, "estoque": 15}
            ]
        }
    }

    titulo: str | None = Field(default=None, min_length=1, max_length=150)
    descricao: str | None = Field(default=None, max_length=2000)
    plataforma: Plataforma | None = None
    genero: str | None = Field(default=None, min_length=1, max_length=50)
    preco: float | None = Field(default=None, gt=0)
    estoque: int | None = Field(default=None, ge=0)
    desenvolvedora: str | None = Field(default=None, max_length=100)
    classificacao_etaria: ClassificacaoEtaria | None = None
    data_lancamento: date | None = None


class JogoResponse(JogoBase):
    # Lê "_id" do Mongo, mas serializa como "id" na resposta.
    id: ObjectIdStr = Field(validation_alias=AliasChoices("_id", "id"))


class JogoListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    itens: list[JogoResponse]
