import sqlite3
from sqlite3 import OperationalError


class UserManager:
    def __init__(self):
        self.db_name = "registration.db"
        self.table_name = "users_data"

    """Создание таблицы"""

    def create_table(self) -> None:
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute(
                f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                    UserID INTEGER PRIMARY KEY,
                    Login TEXT UNIQUE NOT NULL,
                    Password TEXT NOT NULL,
                    Code TEXT NOT NULL);
                """
            )

    """Проверка уникальности логина"""

    def is_login_unique(self, login: str) -> bool:
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute(
                f"""SELECT 1
                        FROM {self.table_name}
                        WHERE LOWER(Login) = ?;
                    """,
                (login.lower(),),
            )
            existing_user = cur.fetchone()
            return existing_user is None

    """Добавление нового пользователя в БД"""

    def add_new_user(self, login: str, password: str, code: str) -> None:
        if not login.strip() or not password.strip():
            print("Логин и пароль не могут быть пустыми")
            return

        if len(code) != 4 or not code.isdigit():
            print("Неверный код. Нужно ввести 4-х значное целое число")
            return

        if not self.is_login_unique(login):
            print(f"Логин {login} уже занят. Попробуйте другой.")
            return

        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute(
                f"""INSERT INTO {self.table_name}
                            (Login, Password, Code)
                        VALUES (?, ?, ?);
                    """,
                (login, password, code),
            )
            print(f"Пользователь {login} успешно зарегистрирован")

    """Регистрация нового пользователя"""

    def register_new_user(self) -> None:
        while True:
            login = input("Введите логин: ")
            if not self.is_login_unique(login):
                print(f"Логин {login} уже занят. Попробуйте другой.")
                continue

            password = input("Введите пароль: ")

            while True:
                code = input("Введите 4-х значный код для восстановления: ")
                if len(code) == 4 and code.isdigit():
                    break
                print("Неверный код. Нужно ввести 4-х значное целое число")

            try:
                self.add_new_user(login, password, code)
                break
            except OperationalError as e:
                print(e)

    """Восстановление пароля"""

    def reset_password(self) -> None:
        login = input("Введите ваш логин: ")
        code = input("Введите ваш код восстановления: ")

        with sqlite3.connect(self.db_name) as db:
            try:
                cur = db.cursor()
                cur.execute(
                    f"""SELECT *
                            FROM {self.table_name}
                            WHERE LOWER(Login) = ? AND Code = ?;
                        """,
                    (login.lower(), code),
                )
                user = cur.fetchone()
                if user:
                    while True:
                        new_password = input("Введите новый пароль: ")
                        if not new_password.strip():
                            print("Пароль не может быть пустым")
                            continue
                        cur.execute(
                            f"""UPDATE {self.table_name}
                                    SET Password = ? WHERE LOWER(Login) = ?;
                                """,
                            (new_password, login),
                        )
                        print("Пароль успешно изменен")
                        break
                else:
                    print("Неверный логин или код")
            except OperationalError as e:
                print(f"Ошибка подключения к базе данных: {e}")

    """Авторизация пользователя"""

    def authorize_user(self) -> None:
        while True:
            login = input("Введите логин: ")
            with sqlite3.connect(self.db_name) as db:
                try:
                    cur = db.cursor()
                    cur.execute(
                        f"""SELECT * FROM {self.table_name}
                                WHERE LOWER(Login) = ?;
                            """,
                        (login.lower(),),
                    )

                    user = cur.fetchone()
                    if user:
                        while True:
                            password = input("Введите пароль: ")
                            if user[2] == password:
                                print("Вы успешно авторизованы")
                                return
                            else:
                                print("Неверный пароль")
                                choice = (
                                    input(
                                        "Хотите восстановить пароль? (Да/Нет): "
                                    )
                                    .strip()
                                    .lower()
                                )
                                if choice == "да":
                                    self.reset_password()
                                    return
                                elif choice == "нет":
                                    continue
                                else:
                                    print(
                                        "Неверный выбор. Пожалуйста, введите 'да' или 'нет'."
                                    )
                    else:
                        print("Пользователь не найден")
                        choice = (
                            input("Хотите зарегистрироваться? (Да/Нет): ")
                            .strip()
                            .lower()
                        )
                        if choice == "да":
                            self.register_new_user()
                            return
                        elif choice == "нет":
                            print("Выход из программы")
                            return
                        else:
                            print(
                                "Неверный выбор. Пожалуйста, введите 'да' или 'нет'."
                            )
                except OperationalError as e:
                    print(f"Ошибка подключения к базе данных: {e}")
