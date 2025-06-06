# Сервис доставки посылок

API сервис для управления доставкой посылок с различными типами и расчетом стоимости.

## Функциональность

- Управление типами посылок
- Создание и отслеживание посылок
- Расчет стоимости доставки
- Интеграция с API ЦБ РФ для получения курсов валют
- Кеширование данных в Redis
- Фоновые задачи с Celery

## Технологии

- FastAPI
- SQLAlchemy
- MySQL
- Redis
- Celery
- Pytest

## Установка

1. Клонируйте репозиторий
2. Создайте файл `.env` с настройками:
```
DATABASE_URL=mysql+asyncmy://user:password@db:3306/delivery_db
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
CBR_API_URL=https://www.cbr-xml-daily.ru/daily_json.js
```

## Запуск

Запустите все сервисы и приложение одной командой:
```bash
docker-compose up --build -d
```
При старте стека автоматически выполняются миграции.

## Тестирование

```bash
docker-compose exec app pytest
```

## API Документация

После запуска приложения, документация доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 
