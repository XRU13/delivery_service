from pydantic.v1 import BaseSettings, Field


class RateSettings(BaseSettings):
    redis_host: str = Field('redis', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')
    redis_db:   int = Field(0,    env='REDIS_DB')
    cbr_url:    str = Field('https://www.cbr-xml-daily.ru/daily_json.js', env='CBR_API_URL')
    ttl_seconds: int = Field(3600, env='RATE_TTL_SECONDS')
    sync_mysql: str = 'mysql+pymysql://user:password@localhost:3306/delivery_db'
