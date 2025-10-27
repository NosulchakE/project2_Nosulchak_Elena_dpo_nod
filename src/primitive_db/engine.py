#!/usr/bin/env python3
import shlex
from .utils import load_metadata, save_metadata
from .core import create_table, drop_table

META_FILE = "db_meta.json"
def print_help():
    """ Выводит справочную информацию по командам."""
    print("\n*** Процесс работы с таблицей ***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип>... - создать таблицу")
    print("<command> list_tables        - показать список таблиц")
    print("<command> drop_table <имя_таблицы>        - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация\n")


def run():
    """
    Главный цикл программы. Обрабатывает команды пользователя.
    """
    print("*** Primitive DB ***")
    print("<command> create_table <имя> <колонка: тип>... - сщздать таблицу")
    print("<command> list_tables        - показать список таблиц")
    print("<command> drop_table <имя>        - удалить таблицу")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")

    while True:
        user_input = input(">>>Введите команду: ").strip()
        if not user_input:
            continue
        try:
            args = shlex.split(user_input)
        except ValueError:
            print("Ошибка: некорректный ввод. Попробуй снова.")
            continue

        command = args[0]

        # Загружаем текущие метаданные
        metadata = load_metadata(META_FILE)

        if command == "exit":
            print("Выход из программы...")
            break
        elif command == "help":
            print_help()
            

        elif command == "list_tables":
            if metadata:
                print("Список таблиц: ")
                for table, columns in metadata.items():
                    cols = ",".join([f"{name}:{type}" for name, type_ in columns])
                    print(f" - {table}:{cols}")
            else:
                print("Таблицы отсутствуют")
            continue


        elif command == "create_table":
            if len(args) < 3:
                print("Некорректное значение: недостаточно аргументов. Пример.")
                print("create_table users name:str age:int")
                continue
            table_name = args[1]
            columns =  args[2:]
            metadata = create_table(metadata, table_name, columns)
            save_metadata(META_FILE, metadata)

        elif command == "drop_table":
            if len(args) != 2:
                print("Ошибка. Нужно указать имя таблицы. Пример.")
                print("drop_table users")
                continue
            table_name = args[1]
            metadata = drop_table(metadata, table_name)
            save_metadata(META_FILE, metadata)

        else:
            print(f"Функции '{command}' нет. введите help для справки.")

