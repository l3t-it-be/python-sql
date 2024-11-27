from dataclasses import dataclass
from sqlite3 import OperationalError

from config import config
from exchanger_app import cmds
from exchanger_app.currencies_rates import ExchangeRate
from initialize_bd import Initialization


@dataclass(kw_only=True)
class UserBalance:
    balance_rub: float
    balance_usd: float
    balance_euro: float


class DBManager(Initialization):
    def __init__(self):
        super().__init__('users_balance')

    def create_table(self) -> None:
        """Создание таблицы"""
        script = cmds.CREATE_TABLE_USERS_BALANCE.format(
            table_name=self.table_name
        )
        try:
            self.cursor.execute(script)
        except OperationalError:
            print(config.DATABASE_CONNECTION_ERROR)

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
        except OperationalError:
            print(config.DATABASE_CONNECTION_ERROR)
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

        if from_currency == config.RUB:
            if to_currency == config.USD:
                amount_to_withdraw = round(
                    amount_to_receive * exchange_rate.usd_to_rub, 2
                )
                return (
                    balance[0] >= amount_to_withdraw
                    and balance[1] >= amount_to_receive
                )
            elif to_currency == config.EURO:
                amount_to_withdraw = round(
                    amount_to_receive * exchange_rate.euro_to_rub, 2
                )
                return (
                    balance[0] >= amount_to_withdraw
                    and balance[2] >= amount_to_receive
                )
        elif from_currency == config.USD:
            if to_currency == config.RUB:
                amount_to_withdraw = round(
                    amount_to_receive / exchange_rate.usd_to_rub, 2
                )
                return (
                    balance[1] >= amount_to_withdraw
                    and balance[0] >= amount_to_receive
                )
            elif to_currency == config.EURO:
                amount_to_withdraw = round(
                    amount_to_receive * exchange_rate.usd_to_euro, 2
                )
                return (
                    balance[1] >= amount_to_withdraw
                    and balance[2] >= amount_to_receive
                )
        elif from_currency == config.EURO:
            if to_currency == config.RUB:
                amount_to_withdraw = round(
                    amount_to_receive / exchange_rate.euro_to_rub, 2
                )
                return (
                    balance[2] >= amount_to_withdraw
                    and balance[0] >= amount_to_receive
                )
            elif to_currency == config.USD:
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
            print(config.NULL_OR_NEGATIVE_SUM)
            return

        if from_currency == config.RUB:
            if to_currency == config.USD:
                amount_to_withdraw = round(
                    amount_to_receive * exchange_rate.usd_to_rub, 2
                )
                script = cmds.UPDATE_BALANCE_RUB_TO_USD.format(
                    table_name=self.table_name,
                    amount_to_withdraw=amount_to_withdraw,
                    amount_to_receive=amount_to_receive,
                )
                self.cursor.execute(script, (user_id,))
            elif to_currency == config.EURO:
                amount_to_withdraw = round(
                    amount_to_receive * exchange_rate.euro_to_rub, 2
                )
                script = cmds.UPDATE_BALANCE_RUB_TO_EURO.format(
                    table_name=self.table_name,
                    amount_to_withdraw=amount_to_withdraw,
                    amount_to_receive=amount_to_receive,
                )
                self.cursor.execute(script, (user_id,))

        elif from_currency == config.USD:
            if to_currency == config.RUB:
                amount_to_withdraw = round(
                    amount_to_receive / exchange_rate.usd_to_rub, 2
                )
                script = cmds.UPDATE_BALANCE_USD_TO_RUB.format(
                    table_name=self.table_name,
                    amount_to_withdraw=amount_to_withdraw,
                    amount_to_receive=amount_to_receive,
                )
                self.cursor.execute(script, (user_id,))
            elif to_currency == config.EURO:
                amount_to_withdraw = round(
                    amount_to_receive * exchange_rate.usd_to_euro, 2
                )
                script = cmds.UPDATE_BALANCE_USD_TO_EUR.format(
                    table_name=self.table_name,
                    amount_to_withdraw=amount_to_withdraw,
                    amount_to_receive=amount_to_receive,
                )
                self.cursor.execute(script, (user_id,))

        elif from_currency == config.EURO:
            if to_currency == config.RUB:
                amount_to_withdraw = round(
                    amount_to_receive / exchange_rate.euro_to_rub, 2
                )
                script = cmds.UPDATE_BALANCE_EUR_TO_RUB.format(
                    table_name=self.table_name,
                    amount_to_withdraw=amount_to_withdraw,
                    amount_to_receive=amount_to_receive,
                )
                self.cursor.execute(script, (user_id,))
            elif to_currency == config.USD:
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
            print(config.INCORRECT_CURRENCY)
            return

        print(config.CURRENCY_EXCHANGE_SUCCESSFULLY_COMPLETED)
