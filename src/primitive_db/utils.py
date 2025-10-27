#!/usr/bin/env python3
import json
from pathlib import Path

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


DATA_DIR = Path("data") # директория для файлов и таблиц
DATA_DIR.mkdir(exist_ok=True)

def load_table_data(table_name: str):
    """загружает таблицы из файла"""
    file_path = DATA_DIR/f"{table_name}.json"
    if not file_path.exists():
        return[]

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return[]
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return[]

def save_table_data(table_name: str, data):
    """ Сщхранение таблиц в файл """
    file_path = DATA_DIR/f"{table_name}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
