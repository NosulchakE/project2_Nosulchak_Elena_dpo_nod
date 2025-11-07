#!/usr/bin/env python3
from ..decorators import  handle_db_errors, confirm_action, log_time, create_cacher
from  .utils import load_table_data, save_table_data
import os
from .constants import VALID_TYPES

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

    metadata[table_name] = {"columns: table_columns"}
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


#___CRUD___
@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    """добавляет новую запись в таблицу"""
    if table_name not in metadata:
        raise KeyError(f" таблицы '{table_name}' не существует.")

    table_info = metadata[table_name]
    columns_without_id = [col_name for col_name, _ in table_info['columns'] if col_name != "ID"]

    if len(values) != len(columns_without_id):
        raise ValueError(f"Ожидается {len(columns_without_id)} значений (без ID), получено {len(values)}")

    # Загружаем данные
    table_data = load_table_data(table_name)

    new_id = max((row.get["ID", 0] for row in table_data), default=0) +1

    new_row = {"ID": new_id}
    for (col_name, col_type), val in zip(table_info["columns"][1:], values):
        if col_type == "int":
            val = int(val)
        elif col_type == "bool":
            val = val.lower() in ("true", "1", "yes")
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
    """ Возвращает все записи, либо фильтр по where_clause"""
    # Генерируем ключ для кэша
    key = (tuple(tuple(row.items()) for row in table_data), frozenset(where_clause.items()) if where_clause else None)
    def get_data():
        if where_clause is None:
            return table_data

        result = []
        for row in table_data:
            match = True
            for key, value in where_clause.items():
               if key not in row or str(row[key]) != str(value):
                    match = False
                    break
            if match:
                result.append(row)
        return result
    return cache(key, get_data)


@handle_db_errors
@log_time
def update(table_data, set_clause, where_clause=None):
    """ Обновляет записи по where_clause"""
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

                    row[key] = new_value.lower() in ("true", "1", "yes")
                elif isinstance(current_value, int):
                    row[key] = int(new_value)
                else:
                    row[key] = str(new_value)


            updated_count += 1

    print("Обновлено записей: {updated_count}")
    return table_data


@handle_db_errors
@confirm_action("удаление записей")
@log_time
def delete(table_data, where_clause=None):
    """ Удаляет записи по where_clause """
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
            match = True
            for key, value in where_clause.items():
                if key not in row or str(row[key]) != str(value):
                    match = False
                    break

            if not match:
                new_data.append(row)
            else:
                deleted_count += 1

    print("Удалено записей: {deleted_count")
    return new_data

