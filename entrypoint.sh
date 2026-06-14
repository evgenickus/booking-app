#!/bin/sh
set -e 

if [ "$1" = "tests" ]; then
  echo "Запуск тестов..."
  pytest -v
  echo "Тесты успешно выполнены. Запускаем сервис..."
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000
elif [ "$#" -eq 0  ]; then
  echo "Запуск тестов пропущен. Запускаем сервис..."
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000
fi

