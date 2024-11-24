import sqlite3
from sqlite3 import Connection, Cursor, OperationalError
from typing import Self
from registration_db import cmds


class UserManager:
    def __init__(self):
        self.db_name: str = 'registration.db'
        self.table_name: str = 'users_data'
        self.db: Connection | None = None
        self.cursor: Cursor | None = None

    def __enter__(self) -> Self:
        self.db = sqlite3.connect(self.db_name, autocommit=True)
        self.cursor = self.db.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db is not None:
            self.db.close()

    def create_table(self) -> None:
        """Создание таблицы"""
        try:
            script = cmds.CREATE_TABLE_USERS_DATA.format(
                table_name=self.table_name
            )
            self.cursor.execute(script)
        except OperationalError as e:
            print(f'Ошибка при создании таблицы: {e}')

    def is_login_unique(self, login: str) -> bool:
        """Проверка уникальности логина"""
        script = cmds.ASSERT_LOGIN_IN_SYSTEM.format(table_name=self.table_name)
        self.cursor.execute(script, (login.lower(),))
        existing_user = self.cursor.fetchone()
        return existing_user is None

    def add_new_user(self, login: str, password: str, code: str) -> None:
        """Добавление нового пользователя в БД"""
        if not login.strip() or not password.strip():
            print('Логин и пароль не могут быть пустыми')
            return

        if len(code) != 4 or not code.isdigit():
            print('Неверный код. Нужно ввести 4-х значное целое число')
            return

        if not self.is_login_unique(login):
            print(f'Логин {login} уже занят. Попробуйте другой.')
            return

        try:
            script = cmds.ADD_NEW_USER.format(table_name=self.table_name)
            self.cursor.execute(script, (login, password, code))
            print(f'Пользователь {login} успешно зарегистрирован')
        except OperationalError as e:
            print(f'Ошибка при добавлении пользователя: {e}')

    def register_new_user(self) -> None:
        """Регистрация нового пользователя"""
        while True:
            login = input('Введите логин: ')

            if not self.is_login_unique(login):
                print(f'Логин {login} уже занят. Попробуйте другой.')
                while True:
                    choice = (
                        input('Хотите продолжить? (Да/Нет): ').strip().lower()
                    )
                    if choice == 'да':
                        return
                    elif choice == 'нет':
                        print('Выход из программы')
                        exit()
                    else:
                        print(
                            'Неверный выбор. Пожалуйста, введите "да" или "нет".'
                        )
                        continue

            if not login.strip():
                print('Логин не может быть пустым')
                while True:
                    choice = (
                        input('Хотите продолжить? (Да/Нет): ').strip().lower()
                    )
                    if choice == 'да':
                        return
                    elif choice == 'нет':
                        print('Выход из программы')
                        exit()
                    else:
                        print(
                            'Неверный выбор. Пожалуйста, введите "да" или "нет".'
                        )
                        continue

            password = input('Введите пароль: ')
            if not password.strip():
                print('Пароль не может быть пустым')
                while True:
                    choice = (
                        input('Хотите продолжить? (Да/Нет): ').strip().lower()
                    )
                    if choice == 'да':
                        return
                    elif choice == 'нет':
                        print('Выход из программы')
                        exit()
                    else:
                        print(
                            'Неверный выбор. Пожалуйста, введите "да" или "нет".'
                        )
                        continue

            while True:
                code = input('Введите 4-х значный код для восстановления: ')
                if len(code) == 4 and code.isdigit():
                    break
                print('Неверный код. Нужно ввести 4-х значное целое число')

            try:
                self.add_new_user(login, password, code)
                break
            except OperationalError as e:
                print(f'Ошибка при регистрации пользователя: {e}')

    def reset_password(self) -> None:
        """Восстановление пароля"""
        login = input('Введите ваш логин: ')
        if not login.strip():
            print('Логин не может быть пустым')
            while True:
                choice = input('Хотите продолжить? (Да/Нет): ').strip().lower()
                if choice == 'да':
                    return
                elif choice == 'нет':
                    print('Выход из программы')
                    exit()
                else:
                    print(
                        'Неверный выбор. Пожалуйста, введите "да" или "нет".'
                    )
                    continue

        script = cmds.ASSERT_LOGIN_IN_SYSTEM.format(table_name=self.table_name)
        self.cursor.execute(script, (login.lower(),))
        user = self.cursor.fetchone()

        if user:
            code = input('Введите ваш код восстановления: ')
            script = cmds.ASSERT_LOGIN_MATCHES_CODE.format(
                table_name=self.table_name
            )
            self.cursor.execute(script, (login.lower(), code))
            user_code_match = self.cursor.fetchone()

            if user_code_match:
                while True:
                    new_password = input('Введите новый пароль: ')
                    if not new_password.strip():
                        print('Пароль не может быть пустым')
                        while True:
                            choice = (
                                input('Хотите продолжить? (Да/Нет): ')
                                .strip()
                                .lower()
                            )
                            if choice == 'да':
                                return
                            elif choice == 'нет':
                                print('Выход из программы')
                                exit()
                            else:
                                print(
                                    'Неверный выбор. Пожалуйста, введите "да" или "нет".'
                                )
                                continue

                    try:
                        script = cmds.UPDATE_PASSWORD.format(
                            table_name=self.table_name
                        )
                        self.cursor.execute(
                            script, (new_password, login.lower())
                        )
                        print('Пароль успешно изменен')
                        break
                    except OperationalError as e:
                        print(f'Ошибка подключения к базе данных: {e}')
            else:
                print('Неверный код восстановления')
        else:
            print('Пользователь не найден')
            while True:
                choice = (
                    input('Хотите зарегистрироваться? (Да/Нет): ')
                    .strip()
                    .lower()
                )
                if choice == 'да':
                    self.register_new_user()
                    return
                elif choice == 'нет':
                    print('Выход из программы')
                    exit()
                else:
                    print(
                        'Неверный выбор. Пожалуйста, введите "да" или "нет".'
                    )
                    continue

    def authorize_user(self) -> None:
        """Авторизация пользователя"""
        while True:
            login = input('Введите логин: ')
            if not login.strip():
                print('Логин не может быть пустым')
                while True:
                    choice = (
                        input('Хотите продолжить? (Да/Нет): ').strip().lower()
                    )
                    if choice == 'да':
                        return
                    elif choice == 'нет':
                        print('Выход из программы')
                        exit()
                    else:
                        print(
                            'Неверный выбор. Пожалуйста, введите "да" или "нет".'
                        )
                        continue

            script = cmds.ASSERT_LOGIN_IN_SYSTEM.format(
                table_name=self.table_name
            )
            self.cursor.execute(script, (login.lower(),))
            user = self.cursor.fetchone()
            if user:
                while True:
                    password = input('Введите пароль: ')
                    if not password.strip():
                        print('Пароль не может быть пустым')
                        while True:
                            choice = (
                                input('Хотите продолжить? (Да/Нет): ')
                                .strip()
                                .lower()
                            )
                            if choice == 'да':
                                return
                            elif choice == 'нет':
                                print('Выход из программы')
                                exit()
                            else:
                                print(
                                    'Неверный выбор. Пожалуйста, введите "да" или "нет".'
                                )
                                continue

                    if user[1] == password:
                        print('Вы успешно авторизованы')
                        return
                    else:
                        print('Неверный пароль')
                        while True:
                            choice = (
                                input('Хотите восстановить пароль? (Да/Нет): ')
                                .strip()
                                .lower()
                            )
                            if choice == 'да':
                                self.reset_password()
                                return
                            elif choice == 'нет':
                                print('Выход из программы')
                                exit()
                            else:
                                print(
                                    'Неверный выбор. Пожалуйста, введите "да" или "нет".'
                                )
                                continue
            else:
                print('Пользователь не найден')
                while True:
                    choice = (
                        input('Хотите зарегистрироваться? (Да/Нет): ')
                        .strip()
                        .lower()
                    )
                    if choice == 'да':
                        self.register_new_user()
                        return
                    elif choice == 'нет':
                        print('Выход из программы')
                        exit()
                    else:
                        print(
                            'Неверный выбор. Пожалуйста, введите "да" или "нет".'
                        )
                        continue
