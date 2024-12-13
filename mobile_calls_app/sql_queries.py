import random
from dataclasses import dataclass
from datetime import datetime
from sqlite3 import OperationalError

from config import config
from initialize_bd import Initialization
from mobile_calls_app import cmds
from mobile_calls_app.reports import report


@dataclass(kw_only=True)
class UserData:
    user: str
    balance: int


@dataclass(kw_only=True)
class MobilePrices:
    mts_mts: int
    mts_tele2: int
    mts_yota: int


class MobileCalls(Initialization):
    def __init__(self):
        super().__init__('mobile_balance')
        self.table2_name = 'mobile_price'

    def create_tables(self) -> None:
        """Создание таблиц"""
        script1 = cmds.CREATE_TABLE_MOBILE_BALANCE.format(
            table_name=self.table_name
        )
        script2 = cmds.CREATE_TABLE_MOBILE_PRICE.format(
            table_name=self.table2_name
        )
        for script in [script1, script2]:
            try:
                self.cursor.execute(script)
            except OperationalError:
                print(config.DATABASE_CONNECTION_ERROR)

    def is_user_unique(self, user: str) -> bool:
        """Проверка уникальности имени пользователя"""
        script = cmds.ASSERT_USER_IN_SYSTEM.format(table_name=self.table_name)
        self.cursor.execute(script, (user.lower(),))
        existing_user = self.cursor.fetchone()
        return existing_user is None

    def get_user_id(self, user: str) -> int | None:
        """Получение user_id по имени пользователя"""
        script = cmds.SELECT_USER_ID.format(table_name=self.table_name)
        self.cursor.execute(script, (user.lower(),))
        user_id = self.cursor.fetchone()
        return user_id[0] if user_id else None

    def add_user(self, user_data: UserData) -> int | None:
        """Добавление в таблицу пользователя (если такого еще нет)"""
        if not self.is_user_unique(user_data.user.lower()):
            print(user_data.user, config.USER_ALREADY_EXISTS)
            return self.get_user_id(user_data.user)

        script = cmds.INSERT_USER_DATA.format(table_name=self.table_name)
        try:
            self.cursor.execute(
                script,
                (user_data.user, user_data.balance),
            )
        except OperationalError:
            print(config.DATABASE_CONNECTION_ERROR)
            return None

        user_id = self.cursor.lastrowid
        return user_id

    def are_prices_exist(self) -> bool:
        """Проверка наличия записей в таблице mobile_price"""
        script = cmds.CHECK_PRICES_EXIST.format(table_name=self.table2_name)
        self.cursor.execute(script)
        existing_prices = self.cursor.fetchone()
        return existing_prices is not None

    def add_prices(self, mobile_prices: MobilePrices) -> None:
        """Добавление в таблицу цен на звонки, если таблица пуста"""
        if self.are_prices_exist():
            print(config.PRICES_ALREADY_ADDED)
            return

        script = cmds.ADD_PRICES.format(table_name=self.table2_name)
        try:
            self.cursor.execute(
                script,
                (
                    mobile_prices.mts_mts,
                    mobile_prices.mts_tele2,
                    mobile_prices.mts_yota,
                ),
            )
        except OperationalError:
            print(config.DATABASE_CONNECTION_ERROR)

    def get_random_operator(self) -> tuple[str, int]:
        """Получение случайного оператора из таблицы mobile_price"""
        script = cmds.GET_RANDOM_OPERATOR.format(table_name=self.table2_name)
        self.cursor.execute(script)
        prices = self.cursor.fetchone()

        operators = config.MOBILE_OPERATORS
        operator_name = random.choice(operators)
        operator_index = operators.index(operator_name)
        price_per_minute = prices[
            operator_index + 1
        ]  # Индекс +1, так как 1-й элемент - это PriceID
        return operator_name, price_per_minute

    def update_balance(self, user_id: int, amount: int) -> bool:
        """Обновление баланса пользователя"""
        script = cmds.UPDATE_BALANCE.format(table_name=self.table_name)
        try:
            self.cursor.execute(script, (amount, user_id))
            return True
        except OperationalError:
            print(config.DATABASE_CONNECTION_ERROR)
            return False

    def get_user_balance(self, user_id: int) -> int:
        """Получение баланса пользователя"""
        script = cmds.GET_USER_BALANCE.format(table_name=self.table_name)
        self.cursor.execute(script, (user_id,))
        balance = self.cursor.fetchone()
        return balance[0] if balance else 0

    def perform_daily_call(self, user_id: int, date: datetime) -> None:
        """Выполнение ежедневного звонка"""
        operator, price_per_min = self.get_random_operator()
        count_min = random.randint(1, 10)
        amount = price_per_min * count_min
        balance = self.get_user_balance(user_id)

        if balance >= amount:
            if self.update_balance(user_id, amount):
                report.report_operation(
                    date.strftime('%d-%m-%Y %H:%M:%S'),
                    operator,
                    count_min,
                    amount,
                )
            else:
                print(config.CONNECTION_PROBLEMS)
        else:
            print(config.NOT_ENOUGH_MONEY_ON_BALANCE)
