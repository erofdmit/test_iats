# Используем базовый образ Python 3.8
FROM python:3.11

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости и requirements.txt в контейнер
COPY ./requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы из текущего каталога (где находится Dockerfile) в контейнер
COPY ./main .

# Команда для запуска FastAPI приложения
CMD ["uvicorn", "fapi:app", "--host", "0.0.0.0", "--port", "8000"]
