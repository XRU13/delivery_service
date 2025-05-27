from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class MySQLSettings(BaseSettings):
	# База данных
	DATABASE_URL: str = 'mysql+aiomysql://user:password@localhost:3306/delivery_db'

	class Config:
		env_file = '.env'


class CelerySettings(BaseSettings):
	# Celery
	CELERY_BROKER_URL: str = 'redis://localhost:6379/1'
	CELERY_RESULT_BACKEND: str = 'redis://localhost:6379/2'
	DATABASE_URL: str = 'mysql+aiomysql://user:password@localhost:3306/delivery_db'

	class Config:
		env_file = '.env'
