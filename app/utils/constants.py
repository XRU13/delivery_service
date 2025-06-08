from enum import Enum


class ParcelsConstants(str, Enum):
	"""
	Константы, связанные с обработкой посылок.
	"""
	NOT_MEANT = 'Не рассчитано'


class CookiesConstants(Enum):
	"""
	Константы, используемые для работы с cookie в рамках пользовательской сессии.
	"""
	SESSION_ID = 'session_id'
	MAX_AGE = 60 * 60 * 24 * 30  # 30 дней
