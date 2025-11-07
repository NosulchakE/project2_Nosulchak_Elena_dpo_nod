#!/usr/bin/env python3
from functools import wraps
import time

def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: файл данных не найден. Возможно база данных не инициализирована.")
        except KeyError as e:
            print(f"Ошибка. Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    return wrapper

def confirm_action(action_name):
    """Декоратор_ требует подтверждения перед опасной операцией
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            confirmation = input(f"В уверены, что хотите выполнить '{action_name}'? [y/n]: ").strip().lower()
            if confirmation != 'y':
                print(f"Операция '{action_name}' отменена пользователем")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator



def log_time(func):
    """декоратор для измерения времени выполнения функции
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        elapsed = end_time - start_time
        print(f"Функция '{func.__name__}' выполнилась за {elapsed:3f}секунд.")
        return result
    return wrapper

def create_cacher():
    """Создает замыкание для кэширования результатов
    """
    cache = {}
    def cache_result(key, value_func):
        if key in cache:
            return cache[key]
        result = value_func()
        cache[key] = result
        return result

    return cache_result
