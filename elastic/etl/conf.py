import os

LIMIT = int(os.getenv("ETL_LIMIT", "100"))
TIME_STEEP = int(os.getenv("ETL_TIME_STEEP", "1"))

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))

ES_ADDRESS = os.getenv("ES_ADDRESS")

STORAGE_FILE = "storage/storage.json"

dsl = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": DB_PORT,
}
