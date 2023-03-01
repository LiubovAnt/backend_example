import logging
import os
import time

from conf import TIME_STEEP
from extract.extract import Extract
from load.load import Load
from storage.state import JsonFileStorage, State
from transform.transform import Transform


class ETLprocess:
    # Запускает внутренние компоненты
    def __init__(self, dsl: dict, es_address: str, storage_file: str):
        self.dsl = dsl
        self.es_address = es_address
        self.storage_file = storage_file

    def run(self):
        while True:
            # Поднимаем соединение ELT
            load = Load(self.es_address)
            # Если произошел какой-то сбой и удаление индекса из ES
            if load.refresh_storage:
                # Чистим память и грузим данные занаво
                if os.path.exists(self.storage_file):
                    os.remove(self.storage_file)
                    logging.info("Файл состояния отчищен")

            # Запускаем загрузку информации о перенесенных изменениях
            storage = JsonFileStorage(self.storage_file)
            state_saver = State(storage)

            # Поднимаем соединение с базой данных
            extract = Extract(self.dsl, state_saver)
            # Объявляем трансформер
            transform = Transform()

            # Процесс переноса данных
            for raw_data in extract.get_data():
                docs = transform.run(raw_data)
                load.push_data(docs)

            # Сохраняем инфромацию о том, какие данные перенесли
            for table, last_modified in extract.producter.state_dict.items():
                state_saver.set_state(table, str(last_modified))

            # Закрываем соединения
            extract.db.close()
            load.es_client.transport.close()

            # Спим
            time.sleep(TIME_STEEP)
