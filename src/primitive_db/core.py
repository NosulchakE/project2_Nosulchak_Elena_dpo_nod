#!/usr/bin/env python3

from ..decorators import (
    confirm_action, 
    create_cacher, 
    handle_db_errors, 
    log_time
)
from .constants import VALID_TYPES
from .utils import load_table_data, save_table_data

cache = create_cacher()


@handle_db_errors
def create_table(metadata, table_name, columns):
    """
    Создать таблицу. С проверками
    """
    if table_name in metadata:
        raise ValueError(f"Ошибка: таблица '{table_name}' уже существует.")

    # Проверяем корректность типови формируем структуру
    table_columns = [("ID", "int")]
    for col in columns:
        if ":" not in col:
            raise ValueError(f"Некорректный формат столбца: {col}")
        col_name, col_type = col.split(":", 1)
        if col_type not in VALID_TYPES:
            raise ValueError(f"Некорректный тип данных: {col_type}")
        table_columns.append((col_name, col_type))

    metadata[table_name] = {"columns": table_columns}
    print(f"Таблица '{table_name}' создана. Колонки: {table_columns}")

    return metadata


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """
    Удалить таблицу
    """
    if table_name not in metadata:
        raise KeyError(f"Ошибка: таблицы '{table_name}' не существует.")
    del metadata[table_name]
    print(f"Таблица '{table_name}'успешно удалена")
    return metadata


# ___CRUD___
@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    """добавляет новую запись в таблицу"""
    if table_name not in metadata:
        raise KeyError(f" таблицы '{table_name}' не существует.")

    table_info = metadata[table_name]
    columns_without_id = [
        col_name for col_name, _ in table_info["columns"] if col_name != "ID"
    ]

    if len(values) != len(columns_without_id):
        raise ValueError(
            f"Вместо {len(columns_without_id)} зн.(без ID),имеем {len(values)}"
        )

    # Загружаем данные
    table_data = load_table_data(table_name)
    if not isinstance(table_data, list):
        print(
            f"DEBUG:Ошибка table_data:ожидался list, получен {type(table_data)}"
        )
        table_data = []

    if table_data:
        try:
            new_id = max(row.get("ID", 0) for row in table_data) + 1
        except Exception as e:
            print(f"DEBUG:    Ошибка генерации id: {e}")
            new_id = 1
    else:
        new_id = 1

    new_row = {"ID": new_id}
    for (col_name, col_type), val in zip(table_info["columns"][1:], values):
        if col_type == "int":
            val = int(val)
        elif col_type == "bool":
            str_val = val.lower()
            val = str_val in ("true", "1", "yes")
        elif col_type == "str":
            val = str(val)
        new_row[col_name] = val

    table_data.append(new_row)
    save_table_data(table_name, table_data)
    print(f"Добавлена запись: {new_row}")
    return table_data


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    """Возвращает все записи, либо фильтр по where_clause"""
    if not isinstance(table_data, list):
        print(
            f"DEBUG:тип table_data: ожидался list, получен {type(table_data)}"
        )
        if isinstance(table_data, str):
            print(f"DEBUG:table_data сщдержит строку: {table_data}")
        return []
    # Генерируем ключ для кэша
    key = (
        tuple(tuple(row.items()) for row in table_data),
        frozenset(where_clause.items()) if where_clause else None,
    )

    def get_data():
        if where_clause is None:
            return table_data

        result = []
        for row in table_data:
            if not isinstance(row, dict):
                print(f"DEBUG:Пропускаем некорректную строку: {row}")
                continue
            match = True
            for key, value in where_clause.items():
                if key not in row or str(row[key]) != str(value):
                    match = False
                    break
            if match:
                result.append(row)
        return result
    cached_result = cache(key, get_data)
    if isinstance(cached_result, str):
        print(f"DEBUG: Кеш поврежден, пересчитываем данные")
        return get_data()

    return cached_result



@handle_db_errors
@log_time
def update(table_data, set_clause, where_clause=None):
    """Обновляет записи по where_clause"""
    if not isinstance(table_data, list):
        print(
            f"DEBUG:тип table_data: ожидался list, получен {type(table_data)}"
        )
        return []
    if not table_data:
        print("Таблица пуста")
        return table_data

    updated_count = 0
    for row in table_data:
        match = True
        if where_clause:
            for key, value in where_clause.items():
                if key not in row or str(row[key]) != str(value):
                    match = False
                    break

        if match:
            for key, new_value in set_clause.items():
                if key not in row:
                    raise KeyError(f"столбец '{key}' не существует.")

                current_value = row[key]
                if isinstance(current_value, bool):
                    str_value = str(new_value).lower()
                    if str_value in ("true", "1", "yes"):
                        row[key] = True
                    elif str_value in ("false", "0", "no"):
                        row[key] = False
                    else:
                        print(f" не удалось распознать {new_value} в boolean")

                elif isinstance(current_value, int):
                    try:
                        row[key] = int(new_value)
                    except ValueError:
                        print(f"не удалось преобразовать {new_value} в int")
                else:
                    row[key] = str(new_value)

            updated_count += 1

    print("Обновлено записей: {updated_count}")
    print(f"DEBUG:update возвращает: {type(table_data)} - {table_data}")
    return table_data


@handle_db_errors
@confirm_action("удаление записей")
@log_time
def delete(table_data, where_clause=None):
    """Удаляет записи по where_clause"""
    if not isinstance(table_data, list):
        print(f"DEBUG: ожидался list получен {type(table_data)}")
        return []   
    if not table_data:
        print("Таблица пуста")
        return table_data
    if where_clause is None:
        deleted_count = len(table_data)
        new_data = []
    else:
        new_data = []
        deleted_count = 0

        for row in table_data:
            if not isinstance(row, dict):
                print(f"DEBUG: пропускаем некорректную строку {row}")
                new_data.append(row)
                continue

            match = True
            for key, value in where_clause.items():
                if key not in row or str(row[key]) != str(value):
                    match = False
                    break

            if not match:
                new_data.append(row)
            else:
                deleted_count += 1

    print("Удалено записей: {deleted_count}")
    print(f"DEBUG: delet возвр-ет {len(new_data)} записей")
    return new_data
