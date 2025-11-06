# /usr/bin/env python3
import shlex
from prettytable import PrettyTable
from .utils import load_metadata, save_metadata, load_table_data, save_table_data, METADATA_FILE
from .core import create_table, drop_table, insert, select, update, delete
from .parser import parse_where_clause, parse_set_clause
from ..decorators import handle_db_errors
from .constants import METADATA_FILE

def print_help():
    """ Выводит справочную информацию по командам."""
    print("\n*** Процесс работы с таблицей ***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип>... - создать таблицу")
    print("<command> list_tables        - показать список таблиц")
    print("<command> drop_table <имя_таблицы>        - удалить таблицу")
    print("<command> insert <таблица> <значение1> <значение2>...- вставка записи")
    print("<command> select <таблица>[where...] - выбрать записи")
    print("<command> update <таблица> set...[where...] - обновить записи")
    print("<command> delete <таблица>[where...] - удалить записи")
    print("\nОбщие команды:")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация\n")

def run():
    """
    Главный цикл программы. Обрабатывает команды пользователя.
    """
    # Загружаем текущие метаданные
    metadata = load_metadata()
    print("*** Primitive DB ***")
    print("<command> create_table <имя> <колонка: тип>... - сщздать таблицу")
    print("<command> list_tables        - показать список таблиц")
    print("<command> drop_table <имя>        - удалить таблицу")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация\n")


    while True:
        try:
            user_input = input(">>>Введите команду: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nВыход из программы...")
            break

        if not user_input:
            continue
        parts = shlex.split(user_input)
        if not parts:
            continue
        cmd = parts[0].lower()

        try:
            if cmd == "exit":
                print("Выход из программы...")
                break
            elif cmd == "help":
                print_help()
            

            elif cmd == "list" and len(parts) > 1 and parts[1].lower() == "tables":
          
                if metadata:
                    print("Список таблиц: ")
                    for name, table_info in metadata.items():
                        columns = [f"{col}:{typ}" for col, typ in table_info["columns"]]
                        print(f"- {name}: {columns}") 
                else:
                    print("Таблицы отсутствуют")
            


            elif cmd == "create" and len(parts) > 2 and parts[1].lower() == "table">:
                table_name = parts[2]
                columns = parts[3]
                if not columns:
                    print("Некорректное значение: недостаточно аргументов.")
                    continue
                metedata = create_table(metadata, table_name, columns)
                save_metadata(metedata)

            elif cmd == "drop" and len(parts) > 1 and parts[1].lower() == "table":

                if len(parts) != 3:
                    print("Ошибка. Укажите имя таблицы для удаления")
                    continue
                table_name = parts[2]
                metadata = drop_table(metadata, table_name)
                save_metadata(metadata)

            elif cmd == "insert":
                if len(parts) < 3:
                    print("Ошибка. Укажите имя таблицы и значения для вставки")
                    continue
                table_name = parts[1]
                values = parts[2:]
                insert(metadata, table_name, values)
               

            elif cmd == "select":
                if len(parts) < 2:
                    print("Ошибка. укажите имя таблицы")
                    continue
                table_name = parts[1]
                table_data = load_table_data(table_name)

                where_clause = None
                if "where" in parts:
                    where_index = parts.index("where") 
                    where_str = " ".join(parts[where_index + 1:])
                    try:
                        where_clause = parse_where_clause(where_str)
                    except ValueError as e:
                        print(f"Ошибка: {e}")
                        continue
                rows = select(table_data, where_clause)
                if rows:
                    table = PrettyTable()
                    table.field_names = rows[0].keys()
                    for row in rows:
                        table.add_row(row.values())
                    print(table)
                else:
                    print("Записи не найдены")


            elif cmd == "update":
                if len(parts) < 4 or "set" not in parts:
                    print("Ошибка. Неверный синтаксис update")
                    continue
                table_name = parts[1]
                set_index = parts.index("set") + 1
                if "where" in parts:
                    where_index = parts.index("where")
                    set_str = " ".join(parts[set_index:where_index])
                    where_str = " ".join(parts[where_index +1:])
                    try:
                        where_clause = parse_where_clause(where_str)
                    except ValueError as e:
                        print(f"Ошибка: {e}")
                        continue
                else:
                    set_str = " ".join(parts[set_index:])
                    where_clause = None

                try:
                    set_clause = parse_set_clause(set_str)
                except ValueError as e:
                    print(f"Ошибка: {e}")
                    continue

                table_data = load_table_data(table_name)
                updated_data = update(table_name, set_clause, where_clause)
                if updated_data is not None:
                    save_table_data(table_name, updated_data)

            elif cmd == "delete":
                if len(parts) < 2:
                    print("Ошибка. укажите имя таблицы")
                    continue
                table_name = parts[1]
                table_data = load_table_data(table_name)

                where_clause = None
                if "where" in parts:
                    where_index = parts.index("where") 
                    where_str = " ".join(parts[where_index + 1:])
                    try:
                        where_clause = parse_where_clause(where_str)
                    except ValueError as e:
                        print(f"Ошибка: {e}")
                        continue
                updated_data = delete(table_name, where_clause)
                if updated_data is not None:
                    save_table_data(table_name, table_data)

            else:
                print(f"Функции '{cmd}' нет. попробуйте снова.")

        except Exception as e:
            print(f"ПРоизошла ошибка: {e}")


