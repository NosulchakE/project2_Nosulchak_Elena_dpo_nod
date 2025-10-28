def parse_value(value):
    """ Определяет тип значения и приводит его к нужному """
    value = value.strip()

    # Строковые значения в кавычках
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]

    # Целое число
    if value.isdigit():
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

    raise ValueError(f"Неизвестный формат значения: {value}")

def parse_set_clause(set_string):
    """ преобразует строку в словарь"""
    result = {}
    parts = set_string.split(",")

    for part in parts:
        if "=" not in part:
            raise ValueError(f"Неизвестный синтаксис SET: {part}")

        field, value = part.split("=", 1)
        result[field.strip()] = parse_value(value)

    return result

def parse_where_clause(where_string):
    """ преобразует строку в словарь """
    result = {}
    parts = where_string.split("AND")
    for part in parts:
        if "=" not in part:
            raise ValueError(f"Неизвестный синтаксис WHERE: {part}")
        field, value = part.split("=", 1)
        result[field.strip()] = parse_value(value)

    return result


