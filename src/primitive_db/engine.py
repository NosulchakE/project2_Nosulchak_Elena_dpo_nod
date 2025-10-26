def welcome():
    print("\nПервая попытка запустить проект!\n")
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")

    while True:
        command = input("\nВведите команду: ").strip().lower()
        if command == "help":
            print("\n<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        elif command == "exit":
            print("Выход из программы...")
            break
        else:
            print("Неизвестная команда. Введите 'help' для справки")
