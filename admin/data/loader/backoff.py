import logging
import time
from functools import wraps


def backoff(func, start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    НАТАШ, ВСТАВАЙ, МЫ ВСЕ УРОНИЛИ, ВООБЩЕ ВСЁ.

    Функция для повторного выполнения функции через некоторое время,
    если возникла ошибка.

    Args:
        func: функця
        start_sleep_time: начальное время повтора
        factor: во сколько раз нужно увеличить время ожидания
        border_sleep_time: граничное время ожидания
    Returns:
        Any. результат выполнения функции

    """

    @wraps(func)
    def inner(*args, **kwargs):
        t = start_sleep_time
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as err:
                logging.warning(err)
                logging.info("Повторный вызов функции {func}".format(func=func))
                time.sleep(t)
                t = t * 2**factor
                if t >= border_sleep_time:
                    t = border_sleep_time

    return inner
