#!/usr/bin/env python3
import json
from pathlib import Path
from .constants import DATA_DIR, METADATA_FILE


def load_metadata():
    """
    Загружает данные. Если файл не найден вернет словарь.
    """

    try:
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip() 
            if content:
                data = json.loads(content)
                print(f"DEBUG:  json загружен: {data}")
                return data
            else:
                print(f"DEBUG:  файл пустой")
            return {}
    except FileNotFoundError:
        print(f"DEBUG:  файл не найден")

        return {}
    except json.JSONDecodeError:
        print(f"Ошибка: файл {METADATA_FILE} поврежден или не является JSON.")
        return{}

def save_metadata(data=None):
    """
    Сохраняет переданные файлы в JSON-файл.
    """
    if data is None:
        data = {}

    print(f"DEBUG:    Данные для сохранения:  {data}")
    for key, value in data.items():
        print(f"DEBUG:   {key}:  {type(value)} - {value}")

    METADATA_FILE.parent.mkdir(exist_ok=True)
    try:
        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"DEBUG:    Метаданные успешно сохранены")
    except Exception as e:
        print(f"DEBUG:    Ошибка при сохранении:  {e}")
        try:
            json.dumps(data)
        except Exception as json_error:
            print(f"DEBUG:  Проблема с сериализацией:  {json_error}")


def load_table_data(table_name: str):
    """загружает таблицы из файла"""
    file_path = DATA_DIR/f"{table_name}.json"
    DATA_DIR.mkdir(exist_ok=True)
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
    DATA_DIR.mkdir(exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

