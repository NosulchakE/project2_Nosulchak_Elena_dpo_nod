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
        print(f"Щшибка: таблицы '{table_name}' не существует.")
        return metadata
    del metadata[table_name]
    print(f"Таблица '{table_name}' удалена.")
    return metadata
