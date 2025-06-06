from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from app.adapters.database.settings import MySQLSettings

from app.adapters.database.tables import metadata

# Alembic Config object
config = context.config

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = metadata

settings = MySQLSettings()

def get_url() -> str:
    """
    Берёт DATABASE_URL из настроек и, если в нём указана асинхронная часть,
    отрезает её — чтобы Alembic использовал чистый mysql://... драйвер.
    """
    url: str = settings.DATABASE_URL
    # убираем async-драйвер
    for async_scheme in ('+asyncmy', '+aiomysql', '+asyncmy'):
        if async_scheme in url:
            url = url.replace(async_scheme, '')
    return url

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # Собираем синхронный движок из конфига
    configuration = config.get_section(config.config_ini_section)
    configuration['sqlalchemy.url'] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
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
