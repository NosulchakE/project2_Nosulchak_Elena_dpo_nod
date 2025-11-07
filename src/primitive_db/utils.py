#!/usr/bin/env python3
import json
from pathlib import Path
from .constants import DATA_DIR, METADATA_FILE


def load_metadata():
    """
    Загружает данные. Если файл не найден вернет словарь.
    """
    print(f"DEBUG:  Текущий файл: {Path(__file__).resolve()}")
    print(f"DEBUG:  PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"DEBUG:  Ищем файл по пути: {METADATA_FILE}")
    print(f"DEBUG:  Файл существует: {METADATA_FILE.exists()}")

    if PROJECT_ROOT.exists():
        print(f"DEBUG:  Файлы в корне: {list(PROJECT_ROOT.glob('*.json'))}")
    try:
        with open(METADATA_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()
            print(f"DEBUG:Прочитано из файла: '{content}'") 
            if content:
                data = json.load(content)
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

def save_metadata(data= None):
    """
    Сохраняет переданные файлы в JSON-файл.
    """
    if data is None:
        data = {}
    METADATA_FILE.parent.mkdir(exist_ok=True)
    with open(METADATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)



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

