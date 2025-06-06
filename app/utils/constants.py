from enum import Enum


class ParcelsConstants(str, Enum):
	NOT_MEANT = 'Не рассчитано'


class CookiesConstants(Enum):
	SESSION_ID = 'session_id'
	MAX_AGE = 60 * 60 * 24 * 30  # 30 дней
