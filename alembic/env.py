import os
import sys
from logging.config import dictConfig

from sqlalchemy import create_engine, pool

from alembic import context

# Добавление корневой директории проекта в путь Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import ENGINE_URL
from app.database.models.models import Base

# Настройки журнала (логгирования) для Alembic
config = context.config

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
    }},
    'handlers': {'console': {
        'class': 'logging.StreamHandler',
        'formatter': 'default',
    }},
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
})

# Определение метаданных для миграций
target_metadata = Base.metadata


# Функция для запуска миграций в режиме онлайн
def run_migrations_online(process_revision_directives=None):
    connectable = create_engine(ENGINE_URL, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


# Проверка, запущен ли Alembic в режиме offline
if context.is_offline_mode():
    raise NotImplementedError("Offline mode is not supported in this setup")
else:
    # Запуск миграций в режиме online
    run_migrations_online()
