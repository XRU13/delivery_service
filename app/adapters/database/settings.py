from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class MySQLSettings(BaseSettings):
	"""
	Настройки подключения к основной базе данных MySQL.
	"""

	DATABASE_URL: str = 'mysql+aiomysql://user:password@localhost:3306/delivery_db'

	model_config = {
		'env_file': '.env'
	}


class CelerySettings(BaseSettings):
	"""
	Настройки Celery: брокер сообщений и результат backend.
	Также используется подключение к БД для фоновых задач.
	"""

	CELERY_BROKER_URL: str = 'redis://localhost:6379/1'
	CELERY_RESULT_BACKEND: str = 'redis://localhost:6379/2'
	DATABASE_URL: str = 'mysql+aiomysql://user:password@localhost:3306/delivery_db'

	model_config = {
		'env_file': '.env'
	}
