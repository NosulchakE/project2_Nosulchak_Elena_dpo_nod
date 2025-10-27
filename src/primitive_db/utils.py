#!/usr/bin/env python3
import json

def load_metadata(filepath):
    """
    Загружает данные. Если файл не найден вернет словарь.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Ошибка: файл {filepath} поврежден или не является JSON.")
        return{}

def save_metadata(filepath, data):
    """
    Сохраняет переданные файлы в JSON-файл.
    """
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
