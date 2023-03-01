import abc
import json
from typing import Any, Optional

from backoff import backoff


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        # Сохранить состояние в постоянное хранилище
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        # Загрузить состояние локально из постоянного хранилища
        pass


class JsonFileStorage(BaseStorage):
    @backoff
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path
        try:
            with open(self.file_path, "r"):
                pass
        except FileNotFoundError:
            with open(self.file_path, "w") as f:
                f.write("{}")

    @backoff
    def save_state(self, state: dict) -> None:
        with open(self.file_path, "r") as read:
            json_dict = json.load(read)
            json_dict.update(state)

        with open(self.file_path, "w") as write:
            json.dump(json_dict, write)

    @backoff
    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path, "r") as f:
                json_dict = json.load(f)

        except FileNotFoundError:
            json_dict = {}
        return json_dict


class State:
    # Класс для хранения состояния при работе с данными, чтобы постоянно
    # не перечитывать данные с начала.
    # Здесь представлена реализация с сохранением состояния в файл.
    # В целом ничего не мешает поменять это поведение на работу с
    # БД или распределённым хранилищем.

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        # Установить состояние для определённого ключа
        self.storage.save_state({key: value})

    def get_state(self, key: str) -> Any:
        # Получить состояние по определённому ключу"""
        storage_dict = self.storage.retrieve_state()
        if key in storage_dict:
            return storage_dict[key]
        return None
