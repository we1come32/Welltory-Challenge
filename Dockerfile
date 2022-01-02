# импортируем python
FROM python:latest

# копирование файлов
COPY . .

# установка зависимостей
RUN pip install -r requirements.txt

# создание миграционных файлов вдруг они не загрузились
RUN python manage.py makemigrations

# проведение миграций
RUN python manage.py migrate

# запуск сервера на 8080 порте локалхоста
ENTRYPOINT bash -c "python manage.py runserver 0.0.0.0:8080"