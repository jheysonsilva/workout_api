from fastapi import APIRouter

from workout_api.atleta.controller import router as atleta_router
from workout_api.centro_treinamento.controller import router as centro_router
from workout_api.categorias.controller import router as categoria_router

api_router = APIRouter()
api_router.include_router(atleta_router, prefix="/atletas", tags=["Atletas"])
api_router.include_router(centro_router, prefix="/centros", tags=["Centros de Treinamento"])
api_router.include_router(categoria_router, prefix="/categorias", tags=["Categorias"])
