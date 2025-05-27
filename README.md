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
- PostgreSQL
- Redis
- Celery
- Pytest

## Установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` с настройками:
```
DATABASE_URL=postgresql://user:password@localhost:5432/delivery_db
REDIS_URL=redis://localhost:6379/0
CBR_API_URL=https://www.cbr-xml-daily.ru/daily_json.js
```

## Запуск

1. Запустите базу данных и Redis:
```bash
docker-compose up -d
```

2. Запустите приложение:
```bash
uvicorn app.composites.http_api:app --reload
```

3. Запустите Celery worker:
```bash
celery -A app.tasks.celery_app worker --loglevel=info
```

4. Запустите Celery beat:
```bash
celery -A app.tasks.celery_app beat --loglevel=info
```

## Тестирование

```bash
pytest
```

## API Документация

После запуска приложения, документация доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 