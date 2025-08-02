import asyncio
import os
from logging.config import fileConfig

from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool

from alembic import context
from workout_api.contrib.models import BaseModel
from workout_api.contrib.repository import models  # Importa todos os modelos

from dotenv import load_dotenv
load_dotenv()  # ← Carrega o .env automaticamente

# Configuração do Alembic
config = context.config

# Lê o arquivo alembic.ini (se existir)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadados dos modelos
target_metadata = BaseModel.metadata


def run_migrations_offline() -> None:
    """Executa as migrações no modo offline (sem conectar ao banco)."""
    url = os.getenv("DATABASE_URL")  # ← Usa o valor do .env
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Executa as migrações no modo online."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Configura e executa as migrações com async SQLAlchemy."""
    url = os.getenv("DATABASE_URL")  # ← Usa o valor do .env
    connectable = async_engine_from_config(
        {"sqlalchemy.url": url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def run_migrations_online() -> None:
    """Ponto de entrada para execuções online."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
