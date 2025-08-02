from typing import Annotated
from pydantic import Field
from workout_api.contrib.schemas import BaseSchema

class CentroTreinamentoBase(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King', max_length=100)]
    endereco: Annotated[str, Field(description='Endereço', example='Rua X, Q02')]
    proprietario: Annotated[str, Field(description='Proprietário', example='Marcos')]

class CentroTreinamentoIn(CentroTreinamentoBase):
    pass

class CentroTreinamentoOut(CentroTreinamentoBase):
    pk_id: int

    class Config:
        orm_mode = True
