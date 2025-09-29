# Базовый образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей и устанавливаем пакеты
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект из папки src в контейнер
COPY src/ .

# Экспортируем порт, на котором будет работать Django
EXPOSE 8000

# Команда по умолчанию для запуска Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]