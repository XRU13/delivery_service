from pydantic import Field
from pydantic_settings import BaseSettings

class RateSettings(BaseSettings):
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