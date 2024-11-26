from sqlite3 import OperationalError

from config import ConfigStrings
from initialize_bd import Initialization
from registration_app import cmds
from registration_app.validations import Validation

validations = Validation()
config = ConfigStrings()


class UserManager(Initialization):
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self.table_name = 'users_data'

    def create_table(self) -> None:
        """Создание таблицы"""
        script = cmds.CREATE_TABLE_USERS_DATA.format(
            table_name=self.table_name
        )
        try:
            self.cursor.execute(script)
        except OperationalError:
            print(config.DATABASE_CONNECTION_ERROR)

    def is_login_unique(self, login: str) -> bool:
        """Проверка уникальности логина"""
        script = cmds.ASSERT_LOGIN_IN_SYSTEM.format(table_name=self.table_name)
        self.cursor.execute(script, (login.lower(),))
        existing_user = self.cursor.fetchone()
        if existing_user:
            print(login, config.LOGIN_ALREADY_EXISTS)
            return False
        return True

    def add_new_user(self, login: str, password: str, code: str) -> None:
        """Добавление нового пользователя в БД"""
        while True:
            if not validations.login_password_are_not_empty(login, password):
                return
            if not validations.validate_code(code):
                return
            if not self.is_login_unique(login):
                return
            break

        script = cmds.ADD_NEW_USER.format(table_name=self.table_name)
        try:
            self.cursor.execute(script, (login, password, code))
            print(config.SUCCESSFUL_REGISTRATION, login)
        except OperationalError:
            print(config.DATABASE_CONNECTION_ERROR)

    def register_new_user(self) -> None:
        """Регистрация нового пользователя"""
        while True:
            login = input(config.INPUT_LOGIN)
            if not validations.check_login_not_null(login):
                continue
            if not self.is_login_unique(login):
                continue

            while True:
                password = input(config.INPUT_PASSWORD)
                if not validations.check_password_not_null(password):
                    continue

                while True:
                    code = input(config.INPUT_CODE)
                    if not validations.validate_code(code):
                        continue

                    try:
                        self.add_new_user(login, password, code)
                        return
                    except OperationalError:
                        print(config.DATABASE_CONNECTION_ERROR)
                        continue

    def reset_password(self) -> None:
        """Восстановление пароля"""
        while True:
            login = input(config.INPUT_LOGIN)
            if not validations.check_login_not_null(login):
                continue

            script = cmds.ASSERT_LOGIN_IN_SYSTEM.format(
                table_name=self.table_name
            )
            self.cursor.execute(script, (login.lower(),))
            user = self.cursor.fetchone()

            if user:
                while True:
                    code = input(config.INPUT_YOUR_CODE)
                    if not validations.validate_code(code):
                        continue

                    script = cmds.ASSERT_LOGIN_MATCHES_CODE.format(
                        table_name=self.table_name
                    )
                    self.cursor.execute(script, (login.lower(), code))
                    user_code_match = self.cursor.fetchone()

                    if user_code_match:
                        while True:
                            new_password = input(config.INPUT_NEW_PASSWORD)
                            if not validations.check_password_not_null(
                                new_password
                            ):
                                continue

                            script = cmds.UPDATE_PASSWORD.format(
                                table_name=self.table_name
                            )
                            try:
                                self.cursor.execute(
                                    script, (new_password, login.lower())
                                )
                                print(config.PASSWORD_SUCCESSFULLY_CHANGED)
                                return  # Завершение выполнения метода после успешной смены пароля
                            except OperationalError:
                                print(config.DATABASE_CONNECTION_ERROR)
                    else:
                        print(config.INCORRECT_CODE)
            else:
                print(config.USER_NOT_FOUND)
                validations.register_or_not(self.register_new_user)

    def authorize_user(self) -> None:
        """Авторизация пользователя"""
        while True:
            login = input(config.INPUT_LOGIN)
            if not validations.check_login_not_null(login):
                continue

            script = cmds.ASSERT_LOGIN_IN_SYSTEM.format(
                table_name=self.table_name
            )
            self.cursor.execute(script, (login.lower(),))
            user = self.cursor.fetchone()

            if user:
                while True:
                    password = input(config.INPUT_PASSWORD)
                    if not validations.check_password_not_null(password):
                        continue

                    if user[1] == password:
                        print(config.SUCCESSFULLY_AUTHORIZED)
                        return
                    else:
                        print(config.INCORRECT_PASSWORD)
                        validations.reset_password_or_not(self.reset_password)
            else:
                print(config.USER_NOT_FOUND)
                validations.register_or_not(self.register_new_user)
