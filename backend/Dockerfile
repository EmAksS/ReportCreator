FROM python:3.10-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Команда для запуска (измените на вашу)
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]