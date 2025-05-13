# Importar DATABASE_URL, Base
from app.database import Base
from app.config import DATABASE_URL

# Modelos para la migración
from app.models import Usuario, Alimento, Intercambio

import sys
import os

# Importaciones por defecto de alembic
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# 1) Alembic Config object, lee valores de 'alembic.ini'
config = context.config

# 2) Configurar logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3) Ajuste para importar desde 'app/'
# Esto supone que 'alembic/' está al mismo nivel que 'app/'
# NutriSwap models metadata
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)

# 4) Establece la URL de conexión en la configuración de Alembic
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# 5) Define el metadata para el 'autogenerate'
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
