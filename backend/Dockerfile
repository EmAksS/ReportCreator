FROM python:3.10-slim

WORKDIR /app

# Устанавливаем русские локали
RUN apt-get update && apt-get install -y locales && \
    sed -i 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen ru_RU.UTF-8

# Устанавливаем переменные окружения для локалей
ENV LANG=ru_RU.UTF-8 \
    LANGUAGE=ru_RU.UTF-8 \
    LC_ALL=ru_RU.UTF-8

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Команда для запуска (измените на вашу)
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]