# Образ, от которого идет наследование
FROM python:3.10.3-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Устанавливаем зависимости 
COPY /app/requirements.txt /app/
RUN pip install --upgrade pip && pip3 install --no-cache-dir -r /app/requirements.txt
# Добавляем внутрь образа папку с приложением 
COPY ./app /app
COPY ./entrypoint.sh /entrypoint.sh
# Рабочая директория для CMD и ENTRYPOINT
WORKDIR /app
RUN chmod +x /entrypoint.sh
# run entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

    