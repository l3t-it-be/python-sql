import sqlite3
from sqlite3 import OperationalError
from typing import Tuple


class SQLAtm:
    def __init__(self):
        self.db_name = 'atm.db'
        self.table_name = 'users_data'

    """Создание таблицы"""

    def create_table(self) -> None:
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute(
                f"""CREATE TABLE IF NOT EXISTS {self.table_name}
                (
                    UserID INTEGER PRIMARY KEY,
                    CardNumber INTEGER NOT NULL,
                    PinCode INTEGER NOT NULL,
                    Balance INTEGER NOT NULL,
                    IsBlocked INTEGER DEFAULT 0
                );
                """
            )

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
            with sqlite3.connect(self.db_name) as db:
                cur = db.cursor()
                cur.execute(
                    f"""SELECT CardNumber, IsBlocked
                        FROM {self.table_name}
                        WHERE CardNumber = ?;
                    """,
                    (card_number,),
                )
                result = cur.fetchone()
                if result is None:
                    print('Введен неизвестный номер карты')
                    return False
                elif result[1] == 1:
                    print('Карта заблокирована')
                    return False
                else:
                    print(f'Введена карта с номером {card_number}')
                    return True
        except OperationalError:
            print('Введен неизвестный номер карты')
            return False

    """Ввод и проверка пин-кода"""

    def input_code(self, card_number: str) -> bool:
        attempts = 3
        while attempts > 0:
            pin_code = input('Введите пин-код: ')
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
                        print('Введен верный пин-код')
                        return True
                    else:
                        attempts -= 1
                        print(
                            f'Неверный пин-код. Осталось попыток: {attempts}'
                        )
                except ValueError:
                    attempts -= 1
                    print(f'Неверный пин-код. Осталось попыток: {attempts}')

        # Блокировка карты после трех неудачных попыток
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute(
                f"""UPDATE users_data
                        SET IsBlocked = 1
                        WHERE CardNumber = ?;
                    """,
                (card_number,),
            )
        print('Карта заблокирована')
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
            print(f'Баланс вашей карты: {result[0]} руб.')

    """Снятие денежных средств с баланса карты"""

    def withdraw_money(self, card_number: str) -> bool:
        while True:
            try:
                amount = input('Введите сумму, которую желаете снять: ')
                if int(amount) <= 0:
                    print('Некорректное значение суммы денежных средств')
                    continue
                else:
                    break
            except ValueError:
                print('Некорректное значение')
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
                print('На вашей карте недостаточно денежных средств')
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
                amount = input('Введите сумму, которую желаете внести: ')
                if int(amount) <= 0:
                    print('Некорректное значение суммы денежных средств')
                    continue
                else:
                    break
            except ValueError:
                print('Некорректное значение')
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
