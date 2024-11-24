from enum import StrEnum
from registration_db.enums import OperationChoice
from registration_db.sql_queries import UserManager


class Operation:
    @staticmethod
    def choose_operation() -> None:
        while True:
            print('Выберите действие:')
            print('1. Регистрация')
            print('2. Авторизация')
            print('3. Восстановление пароля')
            print('4. Выход')

            choice = input('Введите номер действия: ')

            with UserManager() as user:
                if choice == OperationChoice.REGISTER_NEW_USER:
                    user.register_new_user()
                elif choice == OperationChoice.AUTHORIZE_USER:
                    user.authorize_user()
                elif choice == OperationChoice.RESET_PASSWORD:
                    user.reset_password()
                elif choice == OperationChoice.EXIT:
                    print('Выход из программы.')
                    break
                else:
                    print('Некорректное число')
