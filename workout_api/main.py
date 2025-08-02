from fastapi import FastAPI
from fastapi_pagination import add_pagination
from workout_api.atleta.controller import router as atleta_router
from workout_api.categorias.controller import router as categoria_router
from workout_api.centro_treinamento.controller import router as centro_router

app = FastAPI(title='Workout API')

app.include_router(atleta_router, prefix='/atletas', tags=['Atletas'])
app.include_router(categoria_router, prefix='/categorias', tags=['Categorias'])
app.include_router(centro_router, prefix='/centros_treinamento', tags=['Centros de Treinamento'])

add_pagination(app)
