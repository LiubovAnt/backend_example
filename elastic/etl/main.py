import logging

from conf import ES_ADDRESS, STORAGE_FILE, dsl
from etl import ETLprocess

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    process = ETLprocess(dsl, ES_ADDRESS, STORAGE_FILE)
    process.run()
