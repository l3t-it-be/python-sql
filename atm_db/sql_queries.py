import sqlite3
from sqlite3 import Connection, Cursor, OperationalError
from typing import Self, Tuple

import cmds


class SQLAtm:
    def __init__(
        self, db_name: str = "atm.db", table_name: str = "users_data"
    ):
        self.db_name = db_name
        self.table_name = table_name
        self.db: Connection | None = None
        self.cursor: Cursor | None = None

    def __enter__(self) -> Self:
        self.db = sqlite3.connect(self.db_name)
        self.cursor = self.db.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.db is not None:
            self.db.close()

    def create_table(self) -> None:
        """Создание таблицы."""

        script = cmds.CREATE_TABLE_USERS.format(table_name=self.table_name)
        self.cursor.execute(script)

    """Добавление в таблицу пользователя, если пользователя с таким логином еще нет"""

    def add_new_user(self, users_data: Tuple[int, int, int]) -> None:
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute(
                f"""SELECT CardNumber 
                        FROM {self.table_name}
                        WHERE CardNumber = ?;
                    """,
                (users_data[0],),
            )
            user = cur.fetchone()
            if user is None:
                cur.execute(
                    f"""INSERT INTO {self.table_name}
                                (CardNumber, PinCode, Balance)
                            VALUES
                                (?, ?, ?);
                        """,
                    users_data,
                )

    """Ввод и проверка карты"""

    def insert_card(self, card_number: str) -> bool:
        try:
            self.cursor.execute(
                f"""SELECT CardNumber, IsBlocked
                    FROM {self.table_name}
                    WHERE CardNumber = ?;
                """,
                (card_number,),
            )
        except OperationalError:
            print("Введен неизвестный номер карты")
            return False

        return self._check_result(card_number)

    def _check_result(self, card_number: str):
        result = self.cursor.fetchone()
        if result is None:
            print("Введен неизвестный номер карты")
            return False

        if result[1] == 1:
            print("Карта заблокирована")
            return False

        print(f"Введена карта с номером {card_number}")
        return True

    """Ввод и проверка пин-кода"""

    def input_code(self, card_number: str) -> bool:
        attempts = 3
        while attempts > 0:
            pin_code = input("Введите пин-код: ")
            with sqlite3.connect(self.db_name) as db:
                cur = db.cursor()
                cur.execute(
                    f"""SELECT PinCode
                        FROM {self.table_name}
                        WHERE CardNumber = {card_number};
                    """
                )
                result = cur.fetchone()
                try:
                    if int(pin_code) == result[0]:
                        print("Введен верный пин-код")
                        return True
                    else:
                        attempts -= 1
                        print(
                            f"Неверный пин-код. Осталось попыток: {attempts}"
                        )
                except ValueError:
                    attempts -= 1
                    print(f"Неверный пин-код. Осталось попыток: {attempts}")

        # Блокировка карты после трех неудачных попыток
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute(
                """UPDATE users_data
                        SET IsBlocked = 1
                        WHERE CardNumber = ?;
                    """,
                (card_number,),
            )
        print("Карта заблокирована")
        return False

    """Вывод на экран баланса карты"""

    def show_balance(self, card_number: str) -> None:
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute(
                f"""SELECT Balance
                    FROM {self.table_name}
                    WHERE CardNumber = {card_number};
                """
            )
            result = cur.fetchone()
            print(f"Баланс вашей карты: {result[0]} руб.")

    """Снятие денежных средств с баланса карты"""

    def withdraw_money(self, card_number: str) -> bool:
        while True:
            amount = input("Введите сумму, которую желаете снять: ")
            try:
                if int(amount) <= 0:
                    print("Некорректное значение суммы денежных средств")
                    continue
                else:
                    break
            except ValueError:
                print("Некорректное значение")
                return False

        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute(
                f"""SELECT Balance
                    FROM {self.table_name}
                    WHERE CardNumber = {card_number};
                """
            )
            result = cur.fetchone()

            if int(amount) > result[0]:
                print("На вашей карте недостаточно денежных средств")
                return False
            else:
                cur.execute(
                    f"""UPDATE {self.table_name} 
                        SET Balance = Balance - {amount}
                        WHERE CardNumber = {card_number};
                    """
                )

        SQLAtm.show_balance(self, card_number)
        return True

    """Внесение денежных средств на баланс карты"""

    def depositing_money(self, card_number: str) -> bool:
        while True:
            try:
                amount = input("Введите сумму, которую желаете внести: ")
                if int(amount) <= 0:
                    print("Некорректное значение суммы денежных средств")
                    continue
                else:
                    break
            except ValueError:
                print("Некорректное значение")
                return False

        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute(
                f"""UPDATE {self.table_name} 
                    SET Balance = Balance + {amount}
                    WHERE CardNumber = {card_number};
                    """
            )

        SQLAtm.show_balance(self, card_number)
        return True
