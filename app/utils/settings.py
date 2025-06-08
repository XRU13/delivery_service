from pydantic import Field
from pydantic_settings import BaseSettings

class RateSettings(BaseSettings):
    """
    Конфигурация для сервиса получения валютного курса и подключения к Redis/MySQL.

    Атрибуты:
        redis_host (str): Адрес Redis-сервера (по умолчанию — 'redis').
        redis_port (int): Порт Redis-сервера (по умолчанию — 6379).
        redis_db (int): Номер базы данных Redis (по умолчанию — 0).
        cbr_url (str): URL-адрес API Центробанка РФ для получения курса USD→RUB.
        ttl_seconds (int): Время жизни (TTL) курса в Redis-кеше, в секундах.
        sync_mysql (str): Строка подключения к MySQL (синхронная версия).
    """
    redis_host: str = Field(default='redis', validation_alias='REDIS_HOST')
    redis_port: int = Field(default=6379, validation_alias='REDIS_PORT')
    redis_db: int = Field(default=0, validation_alias='REDIS_DB')
    cbr_url: str = Field(default='https://www.cbr-xml-daily.ru/daily_json.js',
                         validation_alias='CBR_API_URL')
    ttl_seconds: int = Field(default=3600, validation_alias='RATE_TTL_SECONDS')
    sync_mysql: str = 'mysql+pymysql://user:password@localhost:3306/delivery_db'

    model_config = {
        'env_file': '.env',
    }