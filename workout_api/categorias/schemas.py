from typing import Annotated
from pydantic import Field
from workout_api.contrib.schemas import BaseSchema

class CategoriaBase(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', example='Scale', max_length=50)]

class CategoriaIn(CategoriaBase):
    pass

class CategoriaOut(CategoriaBase):
    pk_id: int

    class Config:
        orm_mode = True
