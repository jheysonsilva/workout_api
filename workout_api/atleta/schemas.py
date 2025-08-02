from typing import Annotated, Optional
from pydantic import Field, PositiveFloat
from workout_api.contrib.schemas import BaseSchema, OutMixin
from workout_api.categorias.schemas import CategoriaOut
from workout_api.centro_treinamento.schemas import CentroTreinamentoOut

class AtletaBase(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', example='Joao', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example=25)]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example=75.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.70)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]
    categoria_id: Annotated[int, Field(description='ID da categoria do atleta', example=1)]
    centro_treinamento_id: Annotated[int, Field(description='ID do centro de treinamento', example=1)]

class AtletaIn(AtletaBase):
    pass

class AtletaOut(AtletaBase, OutMixin):
    pk_id: int
    categoria: CategoriaOut
    centro_treinamento: CentroTreinamentoOut

    class Config:
        orm_mode = True

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='Joao', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=25)]
    peso: Annotated[Optional[PositiveFloat], Field(None, description='Peso do atleta', example=75.5)]
    altura: Annotated[Optional[PositiveFloat], Field(None, description='Altura do atleta', example=1.70)]
    sexo: Annotated[Optional[str], Field(None, description='Sexo do atleta', example='M', max_length=1)]
    categoria_id: Annotated[Optional[int], Field(None, description='ID da categoria do atleta', example=1)]
    centro_treinamento_id: Annotated[Optional[int], Field(None, description='ID do centro de treinamento', example=1)]
