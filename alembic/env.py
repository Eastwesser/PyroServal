import os
import sys
from logging.config import dictConfig

from alembic import context
from sqlalchemy import create_engine, pool

from app.config import ENGINE_URL

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database.models.models import Base

# Database URL (using psycopg2 instead of asyncpg)
engine_url = ENGINE_URL

# Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Set the SQLAlchemy URL from the engine URL
config.set_main_option('sqlalchemy.url', engine_url)

# Configure the logger
dictConfig({
    "version": 1,
    "formatters": {
        "generic": {
            "format": "%(levelname)-5.5s [%(name)s] %(message)s",
            "datefmt": "%H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "level": "NOTSET",
            "formatter": "generic"
        }
    },
    "root": {
        "level": "WARN",
        "handlers": ["console"]
    },
    "loggers": {
        "alembic": {
            "level": "INFO",
            "handlers": []
        }
    }
})

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    # Create a synchronous engine for migrations
    sync_engine = create_engine(engine_url, poolclass=pool.NullPool)

    with sync_engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
