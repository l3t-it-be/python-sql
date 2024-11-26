import sqlite3
from dataclasses import dataclass
from sqlite3 import Connection, Cursor, OperationalError
from typing import Self

from exchanger_app import cmds
from exchanger_app.currencies_rates import ExchangeRate


@dataclass(kw_only=True)
class UserBalance:
    balance_rub: float
    balance_usd: float
    balance_euro: float


class DBManager:
    def __init__(self):
        self.db_name: str = 'exchanger.db'
        self.table_name: str = 'users_balance'
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
        script = cmds.CREATE_TABLE_USERS_BALANCE.format(
            table_name=self.table_name
        )
        try:
            self.cursor.execute(script)
        except OperationalError as e:
            print(f'Ошибка при создании таблицы: {e}')

    def add_user(self, user_balance: UserBalance) -> int:
        """Добавление в таблицу пользователя"""
        script = cmds.ADD_USER.format(table_name=self.table_name)
        try:
            self.cursor.execute(
                script,
                (
                    user_balance.balance_rub,
                    user_balance.balance_usd,
                    user_balance.balance_euro,
                ),
            )
        except OperationalError as e:
            print(f'Ошибка при добавлении пользователя: {e}')
        user_id = self.cursor.lastrowid
        return user_id

    def is_user_in_system(self, user_id: int) -> bool:
        """Проверка того, что пользователь зарегистрирован в системе"""
        script = cmds.ASSERT_USER_IN_SYSTEM.format(table_name=self.table_name)
        self.cursor.execute(script, (user_id,))

        user = self.cursor.fetchone()
        return bool(user)

    def show_balance(self, user_id: int) -> None:
        """Вывод баланса"""
        script = cmds.SHOW_BALANCE.format(table_name=self.table_name)
        self.cursor.execute(script, (user_id,))
        balance = self.cursor.fetchone()
        print(
            f'Ваш баланс: \n'
            f'RUB - {round(balance[0], 2)}\n'
            f'USD - {round(balance[1], 2)}\n'
            f'EUR - {round(balance[2], 2)}'
        )

    def check_balance(
        self,
        user_id: int,
        from_currency: str,
        to_currency: str,
        amount_to_receive: float,
        exchange_rate: ExchangeRate,
    ) -> bool:
        """Проверка баланса"""
        script = cmds.SHOW_BALANCE.format(table_name=self.table_name)
        self.cursor.execute(script, (user_id,))
        balance = self.cursor.fetchone()

        if from_currency == 'RUB':
            if to_currency == 'USD':
                amount_to_withdraw = round(
                    amount_to_receive * exchange_rate.usd_to_rub, 2
                )
                return (
                    balance[0] >= amount_to_withdraw
                    and balance[1] >= amount_to_receive
                )
            elif to_currency == 'EUR':
                amount_to_withdraw = round(
                    amount_to_receive * exchange_rate.euro_to_rub, 2
                )
                return (
                    balance[0] >= amount_to_withdraw
                    and balance[2] >= amount_to_receive
                )
        elif from_currency == 'USD':
            if to_currency == 'RUB':
                amount_to_withdraw = round(
                    amount_to_receive / exchange_rate.usd_to_rub, 2
                )
                return (
                    balance[1] >= amount_to_withdraw
                    and balance[0] >= amount_to_receive
                )
            elif to_currency == 'EUR':
                amount_to_withdraw = round(
                    amount_to_receive * exchange_rate.usd_to_euro, 2
                )
                return (
                    balance[1] >= amount_to_withdraw
                    and balance[2] >= amount_to_receive
                )
        elif from_currency == 'EUR':
            if to_currency == 'RUB':
                amount_to_withdraw = round(
                    amount_to_receive / exchange_rate.euro_to_rub, 2
                )
                return (
                    balance[2] >= amount_to_withdraw
                    and balance[0] >= amount_to_receive
                )
            elif to_currency == 'USD':
                amount_to_withdraw = round(
                    amount_to_receive * exchange_rate.euro_to_usd, 2
                )
                return (
                    balance[2] >= amount_to_withdraw
                    and balance[1] >= amount_to_receive
                )
            else:
                return False  # Обработка несуществующей валюты

    def exchange_currency(
        self,
        amount_to_receive: float,
        from_currency: str,
        to_currency: str,
        user_id: int,
        exchange_rate: ExchangeRate,
    ) -> None:
        """Обмен валют"""
        if amount_to_receive <= 0:
            print('Нельзя обменивать нулевую или отрицательную сумму.')
            return

        if from_currency == 'RUB':
            if to_currency == 'USD':
                amount_to_withdraw = round(
                    amount_to_receive * exchange_rate.usd_to_rub, 2
                )
                script = cmds.UPDATE_BALANCE_RUB_TO_USD.format(
                    table_name=self.table_name,
                    amount_to_withdraw=amount_to_withdraw,
                    amount_to_receive=amount_to_receive,
                )
                self.cursor.execute(script, (user_id,))
            elif to_currency == 'EUR':
                amount_to_withdraw = round(
                    amount_to_receive * exchange_rate.euro_to_rub, 2
                )
                script = cmds.UPDATE_BALANCE_RUB_TO_EURO.format(
                    table_name=self.table_name,
                    amount_to_withdraw=amount_to_withdraw,
                    amount_to_receive=amount_to_receive,
                )
                self.cursor.execute(script, (user_id,))

        elif from_currency == 'USD':
            if to_currency == 'RUB':
                amount_to_withdraw = round(
                    amount_to_receive / exchange_rate.usd_to_rub, 2
                )
                script = cmds.UPDATE_BALANCE_USD_TO_RUB.format(
                    table_name=self.table_name,
                    amount_to_withdraw=amount_to_withdraw,
                    amount_to_receive=amount_to_receive,
                )
                self.cursor.execute(script, (user_id,))
            elif to_currency == 'EUR':
                amount_to_withdraw = round(
                    amount_to_receive * exchange_rate.usd_to_euro, 2
                )
                script = cmds.UPDATE_BALANCE_USD_TO_EUR.format(
                    table_name=self.table_name,
                    amount_to_withdraw=amount_to_withdraw,
                    amount_to_receive=amount_to_receive,
                )
                self.cursor.execute(script, (user_id,))

        elif from_currency == 'EUR':
            if to_currency == 'RUB':
                amount_to_withdraw = round(
                    amount_to_receive / exchange_rate.euro_to_rub, 2
                )
                script = cmds.UPDATE_BALANCE_EUR_TO_RUB.format(
                    table_name=self.table_name,
                    amount_to_withdraw=amount_to_withdraw,
                    amount_to_receive=amount_to_receive,
                )
                self.cursor.execute(script, (user_id,))
            elif to_currency == 'USD':
                amount_to_withdraw = round(
                    amount_to_receive * exchange_rate.euro_to_usd, 2
                )
                script = cmds.UPDATE_BALANCE_EUR_TO_USD.format(
                    table_name=self.table_name,
                    amount_to_withdraw=amount_to_withdraw,
                    amount_to_receive=amount_to_receive,
                )
                self.cursor.execute(script, (user_id,))
        else:
            print('Неверная валюта')
            return

        print(f'Обмен валюты успешно завершен')
