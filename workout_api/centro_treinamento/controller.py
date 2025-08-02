from typing import Optional
from fastapi import APIRouter, Body, HTTPException, status, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from fastapi_pagination import Page, Params, add_pagination

from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.configs.database import get_session

router = APIRouter()

@router.post(
    '/',
    summary='Criar um novo centro de treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut
)
async def post(
    centro_in: CentroTreinamentoIn = Body(...),
    db_session: AsyncSession = Depends(get_session)
):
    try:
        centro_model = CentroTreinamentoModel(**centro_in.model_dump())
        db_session.add(centro_model)
        await db_session.commit()
        await db_session.refresh(centro_model)
    except IntegrityError as e:
        await db_session.rollback()
        if 'nome' in str(e.orig).lower():
            raise HTTPException(
                status_code=303,
                detail=f"Já existe um centro de treinamento cadastrado com o nome: {centro_in.nome}"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Erro ao inserir o centro de treinamento no banco'
            )
    except Exception:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Erro ao inserir o centro de treinamento no banco'
        )
    return centro_model

@router.get(
    '/',
    summary='Consultar todos os centros de treinamento com filtro e paginação',
    response_model=Page[CentroTreinamentoOut]
)
async def query(
    nome: Optional[str] = Query(None, description="Filtrar por nome do centro de treinamento"),
    params: Params = Depends(),
    db_session: AsyncSession = Depends(get_session)
):
    query = select(CentroTreinamentoModel)
    if nome:
        query = query.filter(CentroTreinamentoModel.nome.ilike(f"%{nome}%"))

    total_result = await db_session.execute(
        select(func.count()).select_from(query.subquery())
    )
    total_count = total_result.scalar_one()

    offset = (params.page - 1) * params.size
    result = await db_session.execute(query.offset(offset).limit(params.size))
    items = result.scalars().all()

    return Page.create(items=items, total=total_count, params=params)

@router.get(
    '/{pk_id}',
    summary='Consulta um centro de treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut
)
async def get(
    pk_id: int,
    db_session: AsyncSession = Depends(get_session)
):
    centro = (await db_session.execute(select(CentroTreinamentoModel).filter_by(pk_id=pk_id))).scalars().first()
    if not centro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Centro de treinamento não encontrado no id: {pk_id}'
        )
    return centro

add_pagination(router)
