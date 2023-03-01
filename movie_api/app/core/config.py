import os
from logging import config as logging_config

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv("PROJECT_NAME", "movies API")

# Настройки Redis
REDIS_HOST = os.getenv("REDIS_HOST", "movie_redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Настройки Elasticsearch
ELASTIC_HOST = os.getenv("ELASTIC_HOST", "es")
ELASTIC_PORT = int(os.getenv("ELASTIC_PORT", 9200))

# Настройки API
API_HOST = os.getenv("API_HOST", "movie_api")
API_PORT = int(os.getenv("API_PORT", 8001))

# Корень проекта
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)),
)
