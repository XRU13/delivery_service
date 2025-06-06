FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    default-mysql-client \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей (отдельно — для кеша)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY alembic.ini .

# Копирование исходников
COPY . .

# Создание пользователя и смена владельца
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Значение по умолчанию — bash (переопределяется в docker-compose)
CMD ['bash']
