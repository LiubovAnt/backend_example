# Образ, от которого идет наследование
FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Рабочая директория для CMD и ENTRYPOINT
WORKDIR /app
# Устанавливаем зависимости 
COPY /app/requirements.txt /app/
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r ./requirements.txt
# Добавляем внутрь образа папку с приложением 
COPY ./app /app
CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000
