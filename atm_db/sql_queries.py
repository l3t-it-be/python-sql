import sqlite3
from dataclasses import dataclass
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

    def create_table(self) -> None:
        """Создание таблицы"""
        script = cmds.CREATE_TABLE_USERS_DATA.format(
            table_name=self.table_name
        )
        try:
            self.cursor.execute(script)
        except OperationalError as e:
            print(f'Ошибка при создании таблицы: {e}')

    def add_new_user(self, users_data: UserData) -> None:
        """Добавление в таблицу пользователя (если такого еще нет)"""
        script = cmds.SELECT_CARD_NUMBER_IF_EXISTS.format(
            table_name=self.table_name
        )
        self.cursor.execute(script, (users_data.card_number,))

        user = self.cursor.fetchone()
        if user is None:
            try:
                script = cmds.INSERT_USERS_DATA.format(
                    table_name=self.table_name
                )
                self.cursor.execute(
                    script,
                    (
                        users_data.card_number,
                        users_data.pin_code,
                        users_data.balance,
                    ),
                )
            except OperationalError as e:
                print(f'Ошибка при добавлении пользователя: {e}')
            else:
                print(
                    'Пользователь с таким номером карты уже зарегистрирован в системе'
                )

    def check_result(self, card_number: str) -> bool:
        """Проверка номера введенной карты"""
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

    def insert_card(self, card_number: str) -> bool:
        """Ввод карты и пин-кода"""
        script = cmds.SELECT_CARD_NUMBER_AND_IsBlocked.format(
            table_name=self.table_name
        )
        self.cursor.execute(script, (card_number,))

        return self.check_result(card_number)

    def input_code(self, card_number: str) -> bool:
        """Проверка пин-кода"""
        attempts = 3
        while attempts > 0:
            pin_code = input('Введите пин-код: ')
            script = cmds.SELECT_PIN_CODE.format(table_name=self.table_name)
            self.cursor.execute(script, (card_number,))
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
        try:
            script = cmds.BLOCK_CARD_NUMBER.format(table_name=self.table_name)
            self.cursor.execute(script, (card_number,))
        except OperationalError as e:
            print(f'Ошибка при блокировке карты: {e}')
        print('Карта заблокирована')
        return False

    def show_balance(self, card_number: str) -> None:
        """Вывод баланса карты"""
        script = cmds.SHOW_BALANCE.format(table_name=self.table_name)
        self.cursor.execute(script, (card_number,))
        result = self.cursor.fetchone()
        if result is not None:
            print(f'Баланс вашей карты: {result[0]} руб.')
        else:
            print('Карта не найдена.')

    def withdraw_money(self, card_number: str) -> bool:
        """Снятие денежных средств с карты"""
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

        script = cmds.SHOW_BALANCE.format(table_name=self.table_name)
        self.cursor.execute(script, (card_number,))
        result = self.cursor.fetchone()

        if int(amount) > result[0]:
            print('На вашей карте недостаточно денежных средств')
            return False
        else:
            try:
                script = cmds.REDUCE_BALANCE.format(
                    table_name=self.table_name, amount=amount
                )
                self.cursor.execute(script, (card_number,))
            except OperationalError as e:
                print(f'Ошибка при списании денежных средств: {e}')

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

        try:
            script = cmds.INCREASE_BALANCE.format(
                table_name=self.table_name, amount=amount
            )
            self.cursor.execute(script, (card_number,))
        except OperationalError as e:
            print(f'Ошибка при пополнении денежных средств: {e}')

        self.show_balance(card_number)
        return True
