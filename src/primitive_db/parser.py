#!/usr/bin/env/ puthon3

def parse_value(value):
    """ Определяет тип значения и приводит его к нужному """
    value = value.strip()

    # Строковые значения в кавычках
    if (value.startswith("'") and value.endswith("'") or value.startswith('"') and value.endswith('"')):
        return value[1:-1]

    # Целое число
    if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
        return int(value)

    # Вещественное число
    try:
        return float(value)
    except ValueError:
        pass

    # Буллево
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False

    raise value

def parse_set_clause(set_string):
    """ преобразует строку в словарь"""
    result = {}
    parts = set_string.split(",")

    for part in parts:
        part = part.strip()
        if "=" not in part:
            raise ValueError(f"Неизвестный синтаксис SET: {part}")

        field, value = part.split("=", 1)
        result[field.strip()] = parse_value(value)

    return result

def parse_where_clause(where_string):
    """ преобразует строку в словарь """
    result = {}
    conditions = where_string.split("AND")
    for conditions in conditions:
        conditions = conditions.strip()
        if "=" not in conditions:
            raise ValueError(f"Неизвестный синтаксис WHERE: {conditions}")
        field, value = conditions.split("=", 1)
        result[field.strip()] = parse_value(value)

    return result


