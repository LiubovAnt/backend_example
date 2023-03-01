# Образ, от которого идет наследование
FROM python:3.10.3-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Рабочая директория для CMD и ENTRYPOINT
WORKDIR /etl
# Устанавливаем зависимости 
COPY /etl/requirements.txt /etl/
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r ./requirements.txt
# Добавляем внутрь образа папку с приложением 
COPY ./etl /etl
RUN chmod +x /etl/entrypoint.sh
ENTRYPOINT ["/etl/entrypoint.sh"]
#CMD python3 main.py
