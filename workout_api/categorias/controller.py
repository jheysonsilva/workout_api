from typing import Optional
from fastapi import APIRouter, Body, HTTPException, status, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func  # IMPORTAÇÃO ESSENCIAL PARA O count()

from fastapi_pagination import Page, Params, add_pagination

from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.categorias.models import CategoriaModel
from workout_api.configs.database import get_session

router = APIRouter()

@router.post(
    '/',
    summary='Criar uma nova categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut
)
async def post(
    categoria_in: CategoriaIn = Body(...),
    db_session: AsyncSession = Depends(get_session)
):
    try:
        categoria_model = CategoriaModel(**categoria_in.model_dump())
        db_session.add(categoria_model)
        await db_session.commit()
        await db_session.refresh(categoria_model)
    except IntegrityError as e:
        await db_session.rollback()
        if 'nome' in str(e.orig).lower():
            raise HTTPException(
                status_code=303,
                detail=f"Já existe uma categoria cadastrada com o nome: {categoria_in.nome}"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Erro ao inserir a categoria no banco'
            )
    except Exception:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Erro ao inserir a categoria no banco'
        )
    return categoria_model

@router.get(
    '/',
    summary='Consultar todas as categorias com filtro e paginação',
    response_model=Page[CategoriaOut]
)
async def query(
    nome: Optional[str] = Query(None, description="Filtrar por nome da categoria"),
    params: Params = Depends(),
    db_session: AsyncSession = Depends(get_session)
):
    query = select(CategoriaModel)
    if nome:
        query = query.filter(CategoriaModel.nome.ilike(f"%{nome}%"))

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
    summary='Consulta uma categoria pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut
)
async def get(
    pk_id: int,
    db_session: AsyncSession = Depends(get_session)
):
    result = await db_session.execute(select(CategoriaModel).filter_by(pk_id=pk_id))
    categoria = result.scalars().first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Categoria não encontrada no id: {pk_id}'
        )
    return categoria

add_pagination(router)
