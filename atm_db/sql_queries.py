from dataclasses import dataclass
import sqlite3
from sqlite3 import OperationalError, Connection, Cursor
from typing import Self
import cmds


@dataclass(kw_only=True)
class UserData:
    card_number: int
    pin_code: int
    balance: int


class SQLAtm:
    def __init__(self):
        self.db_name: str = 'atm.db'
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

    """Создание таблицы"""

    def create_table(self) -> None:
        script = cmds.CREATE_TABLE_USERS_DATA.format(
            table_name=self.table_name
        )
        try:
            self.cursor.execute(script)
        except OperationalError as e:
            print(f'Ошибка при создании таблицы: {e}')

    """Добавление в таблицу пользователя (если такого еще нет)"""

    def add_new_user(self, users_data: UserData) -> None:
        try:
            self.cursor.execute(
                f"""SELECT CardNumber
                        FROM {self.table_name}
                        WHERE CardNumber = ?
                        LIMIT 1;
                """,
                (users_data.card_number,),
            )
            user = self.cursor.fetchone()
            if user is None:
                self.cursor.execute(
                    f"""INSERT INTO {self.table_name}
                                    (CardNumber, PinCode, Balance)
                            VALUES
                                (?, ?, ?);
                        """,
                    (
                        users_data.card_number,
                        users_data.pin_code,
                        users_data.balance,
                    ),
                )
            else:
                print(
                    'Пользователь с таким номером карты уже зарегистрирован в системе'
                )
        except OperationalError as e:
            print(f'Ошибка при добавлении нового пользователя: {e}')

    """Проверка номера введенной карты"""

    def check_result(self, card_number: str) -> bool:
        result = self.cursor.fetchone()
        if result is None:
            print(
                'Введен неизвестный номер карты. Пожалуйста, обратитесь в банк.'
            )
            return False

        if result[1] == 1:
            print('Карта заблокирована')
            return False

        print(f'Введена карта с номером {card_number}')
        return True

    """Ввод карты и пин-кода"""

    def insert_card(self, card_number: str) -> bool:
        try:
            self.cursor.execute(
                f"""SELECT CardNumber, IsBlocked
                        FROM {self.table_name}
                        WHERE CardNumber = ?
                        LIMIT 1;
                    """,
                (card_number,),
            )
        except OperationalError as e:
            print(f'Ошибка при поиске карты: {e}')
            return False

        return self.check_result(card_number)

    def input_code(self, card_number: str) -> bool:
        attempts = 3
        while attempts > 0:
            pin_code = input('Введите пин-код: ')
            self.cursor.execute(
                f"""SELECT PinCode
                        FROM {self.table_name}
                        WHERE CardNumber = ?
                        LIMIT 1;
                    """,
                (card_number,),
            )
            result = self.cursor.fetchone()
            try:
                if int(pin_code) == result[0]:
                    print('Введен верный пин-код')
                    return True
                else:
                    attempts -= 1
                    print(f'Неверный пин-код. Осталось попыток: {attempts}')
            except ValueError:
                attempts -= 1
                print(f'Неверный пин-код. Осталось попыток: {attempts}')

        # Блокировка карты после трех неудачных попыток
        self.cursor.execute(
            f"""UPDATE {self.table_name}
                    SET IsBlocked = True
                    WHERE CardNumber = ?;
                    """,
            (card_number,),
        )
        print('Карта заблокирована')
        return False

    """Вывод баланса карты"""

    def show_balance(self, card_number: str) -> None:
        try:
            self.cursor.execute(
                f"""SELECT Balance
                        FROM {self.table_name}
                        WHERE CardNumber = ?
                        LIMIT 1;
                    """,
                (card_number,),
            )
            result = self.cursor.fetchone()
            if result is not None:
                print(f'Баланс вашей карты: {result[0]} руб.')
            else:
                print('Карта не найдена.')
        except OperationalError as e:
            print(f'Ошибка при получении баланса: {e}')

    """Снятие денежных средств с карты"""

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

        self.cursor.execute(
            f"""SELECT Balance
                    FROM {self.table_name}
                    WHERE CardNumber = ?;
                    """,
            (card_number,),
        )
        result = self.cursor.fetchone()

        if int(amount) > result[0]:
            print('На вашей карте недостаточно денежных средств')
            return False
        else:
            self.cursor.execute(
                f"""UPDATE {self.table_name}
                        SET Balance = Balance - ?
                        WHERE CardNumber = ?;
                """,
                (amount, card_number),
            )

        self.show_balance(card_number)
        return True

    """Внесение денежных средств на карту"""

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

        self.cursor.execute(
            f"""UPDATE {self.table_name}
                    SET Balance = Balance + ?
                    WHERE CardNumber = ?;
                """,
            (amount, card_number),
        )

        self.show_balance(card_number)
        return True
