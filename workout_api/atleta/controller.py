from typing import Optional
from fastapi import APIRouter, Body, HTTPException, status, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from fastapi_pagination import Page, Params, add_pagination

from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.configs.database import get_session

router = APIRouter()


@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def create_atleta(
    atleta_in: AtletaIn = Body(...),
    db_session: AsyncSession = Depends(get_session)
):
    # Verificar existência de categoria
    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(pk_id=atleta_in.categoria_id))
    ).scalars().first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Categoria com id {atleta_in.categoria_id} não encontrada.'
        )

    # Verificar existência de centro de treinamento
    centro = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(pk_id=atleta_in.centro_treinamento_id))
    ).scalars().first()
    if not centro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Centro de treinamento com id {atleta_in.centro_treinamento_id} não encontrado.'
        )

    try:
        atleta_model = AtletaModel(**atleta_in.model_dump())
        db_session.add(atleta_model)
        await db_session.commit()
        await db_session.refresh(atleta_model)
    except IntegrityError as e:
        await db_session.rollback()
        if 'cpf' in str(e.orig).lower():
            raise HTTPException(
                status_code=303,
                detail=f"Já existe um atleta cadastrado com o CPF: {atleta_in.cpf}"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Erro ao inserir dados no banco'
            )
    except Exception:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Erro ao inserir dados no banco'
        )

    return AtletaOut.from_orm(atleta_model)


@router.get(
    '/',
    summary='Listar atletas com filtros e paginação',
    response_model=Page[AtletaOut]
)
async def list_atletas(
    nome: Optional[str] = Query(None, description='Filtrar por nome do atleta'),
    cpf: Optional[str] = Query(None, description='Filtrar por CPF do atleta'),
    params: Params = Depends(),
    db_session: AsyncSession = Depends(get_session)
):
    query = select(AtletaModel)

    if nome:
        query = query.filter(AtletaModel.nome.ilike(f'%{nome}%'))

    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)

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
    summary='Obter atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut
)
async def get_atleta(
    pk_id: int,
    db_session: AsyncSession = Depends(get_session)
):
    atleta = (await db_session.execute(
        select(AtletaModel).filter_by(pk_id=pk_id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado para o id {pk_id}'
        )

    return AtletaOut.from_orm(atleta)


@router.patch(
    '/{pk_id}',
    summary='Atualizar parcialmente atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut
)
async def update_atleta(
    pk_id: int,
    atleta_up: AtletaUpdate = Body(...),
    db_session: AsyncSession = Depends(get_session)
):
    atleta = (await db_session.execute(
        select(AtletaModel).filter_by(pk_id=pk_id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado para o id {pk_id}'
        )

    dados_update = atleta_up.model_dump(exclude_unset=True)

    if 'categoria_id' in dados_update:
        categoria = (await db_session.execute(
            select(CategoriaModel).filter_by(pk_id=dados_update['categoria_id']))
        ).scalars().first()
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Categoria com id {dados_update["categoria_id"]} não encontrada.'
            )

    if 'centro_treinamento_id' in dados_update:
        centro = (await db_session.execute(
            select(CentroTreinamentoModel).filter_by(pk_id=dados_update['centro_treinamento_id']))
        ).scalars().first()
        if not centro:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Centro de treinamento com id {dados_update["centro_treinamento_id"]} não encontrado.'
            )

    for chave, valor in dados_update.items():
        setattr(atleta, chave, valor)

    try:
        await db_session.commit()
        await db_session.refresh(atleta)
    except IntegrityError as e:
        await db_session.rollback()
        if 'cpf' in str(e.orig).lower():
            raise HTTPException(
                status_code=303,
                detail=f"Já existe um atleta cadastrado com o CPF: {dados_update.get('cpf')}"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Erro ao atualizar dados no banco'
            )
    except Exception:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Erro ao atualizar dados no banco'
        )

    return AtletaOut.from_orm(atleta)


@router.delete(
    '/{pk_id}',
    summary='Deletar atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_atleta(
    pk_id: int,
    db_session: AsyncSession = Depends(get_session)
):
    atleta = (await db_session.execute(
        select(AtletaModel).filter_by(pk_id=pk_id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado para o id {pk_id}'
        )

    await db_session.delete(atleta)
    await db_session.commit()


add_pagination(router)
