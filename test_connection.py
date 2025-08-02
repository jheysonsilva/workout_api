import asyncio
from workout_api.db import engine
from workout_api.contrib.models import Base  # Base geral usada pelos models

async def create_db():
    async with engine.begin() as conn:
        print("Conectando ao banco de dados...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    asyncio.run(create_db())
