#!/bin/bash

# Ждем готовности базы данных (10 секунд)
echo "Ожидание готовности базы данных (10 секунд)..."
sleep 10
echo "База данных должна быть готова!"

# Применяем миграции
echo "Применение миграций..."
alembic upgrade head

# Запускаем приложение
echo "Запуск приложения..."
gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
