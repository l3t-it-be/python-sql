from sql_queries import UserManager


class Operation:
    @staticmethod
    def choose_operation():
        user = UserManager()
        while True:
            print("Выберите действие:")
            print("1. Регистрация")
            print("2. Авторизация")
            print("3. Восстановление пароля")
            print("4. Выход")

            choice = input("Введите номер действия: ")

            if choice == "1":
                user.register_new_user()
            elif choice == "2":
                user.authorize_user()
            elif choice == "3":
                user.reset_password()
            elif choice == "4":
                print("Выход из программы.")
                break
            else:
                print("Некорректное число")
