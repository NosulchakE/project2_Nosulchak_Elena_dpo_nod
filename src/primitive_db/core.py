#!/usr/bin/env python3
VALID_TYPES = {"int", "str", "bool"}

def create_table(metadata, table_name, columns):
    """
    Создать таблицу.
    :param metadata: словарь метаданных (все таблицы)
    :param table_name: имя новой таблицы
    :param columns: список строк вида ["name:str", "age:int"]
    :return: обновленный metadata
    """
    if table_name in metadata:
        print(f"Ошибка: таблица '{table_name}' уже существует.")
        return metadata

    has_id = False
    cleaned_columns = []

    for col in columns:
        if ":" not in col:
            print(f"Ошибка: неправильный формат столбца '{col}'. Используйте <имя:тип>.")
            return metadata

        name, col_type = col.split(":", 1)
        name = name.strip()
        col_type = col_type.strip()

        if col_type not in VALID_TYPES:
            print(f"Ошибка: тип '{col_type}' некорректен. Допустимо: {','.join(VALID_TYPES)}")
            return  metadata

        if name.lower() == "id":
            if col_type != "int":
                print("Ошибка: столбец должен иметь тип int")
                return  metadata
            has_id = True

        cleaned_columns.append(f"{name}:{col_type}")

    if not has_id:
        cleaned_columns.insert(0, "ID:int")

    metadata[table_name] = cleaned_columns
    print(f"Таблица '{table_name}' создана. Колонки: {cleaned_columns}")
    return metadata


def drop_table(metadata, table_name):
    """
    Удалить таблицу
    """
    if table_name not in metadata:
        print(f"Ошибка: таблицы '{table_name}' не существует.")
        return metadata
    del metadata[table_name]
    print(f"Таблица '{table_name}' удалена.")
    return metadata

#___CRUD___

def insert(metadata, table_name, values, table_data):
    """добавляет новую запись в таблицу"""
    if table_name not in metadata:
        print(f"Ошибка: таблицы '{table_name}' не существует.")
        return table_data

    columns = metadata[table_name]
    non_id_columns = columns[1:]
    if len(values) != len(non_id_columns):
        print("Ошибка: количество значений не соответствует количеству столбцов")
        return table_data

    new_record = {}
    if table_data:
        new_id = max(row["ID"] for row in table_data) = 1
    else:
        new_id = 1
    new_record[!ID"] = new_id

    for col_def, val in zip(non_id_columns, values):
        name, col_type = col_def.split(":")
        try:
            if col_type == "int":
                val = int(val)
            elif col_type == "str":
                val = str(val)
            elif col_type == "bool"
                val = bool(val)
        except ValueError:
            print(f"Некорректное значение: {val} для {col_type}")
            return table_data
        new_record[name] = val

    table_data.append(new_record)
    print(f"Добавлена запись: {new_record}")
    return table_data

def select(table_data, where_clause=None):

