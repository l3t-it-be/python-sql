from dataclasses import dataclass
from sqlite3 import OperationalError

from config import config
from initialize_bd import Initialization
from mobile_app import cmds


@dataclass(kw_only=True)
class UserData:
    user_name: str
    balance: int
    tariff_ref: int


@dataclass(kw_only=True)
class TariffData:
    tariff: str
    price: int


class MobileUsers(Initialization):
    def __init__(self):
        super().__init__('mobile_users')
        self.table2_name = 'mobile_tariff'

    def create_tables(self) -> None:
        """Создание таблиц"""
        script1 = cmds.CREATE_TABLE_MOBILE_USERS.format(
            table_name=self.table_name
        )
        script2 = cmds.CREATE_TABLE_MOBILE_TARIFFS.format(
            table_name=self.table2_name
        )
        for script in [script1, script2]:
            try:
                self.cursor.execute(script)
            except OperationalError:
                print(config.DATABASE_CONNECTION_ERROR)

    def is_user_name_unique(self, user_name: str) -> bool:
        """Проверка уникальности логина"""
        script = cmds.ASSERT_USER_NAME_IN_SYSTEM.format(
            table_name=self.table_name
        )
        self.cursor.execute(script, (user_name.lower(),))
        existing_user = self.cursor.fetchone()
        return existing_user is None

    def is_tariff_unique(self, tariff: str) -> bool:
        """Проверка уникальности тарифа"""
        script = cmds.ASSERT_TARIFF_IN_SYSTEM.format(
            table_name=self.table2_name
        )
        self.cursor.execute(script, (tariff.lower(),))
        existing_tariff = self.cursor.fetchone()
        return existing_tariff is None

    def add_user(self, user_data: UserData) -> None:
        """Добавление в таблицу пользователя (если такого еще нет)"""
        if not self.is_user_name_unique(user_data.user_name.lower()):
            print(user_data.user_name, config.USER_ALREADY_EXISTS)
            return

        script = cmds.INSERT_USERS_DATA.format(table_name=self.table_name)
        try:
            self.cursor.execute(
                script,
                (user_data.user_name, user_data.balance, user_data.tariff_ref),
            )
        except OperationalError:
            print(config.DATABASE_CONNECTION_ERROR)

    def add_tariff(self, tariff_data: TariffData) -> None:
        """Добавление в таблицу тарифа (если такого еще нет)"""
        if not self.is_tariff_unique(tariff_data.tariff.lower()):
            print(tariff_data.tariff, config.TARIFF_ALREADY_EXISTS)
            return

        script = cmds.ADD_TARIFF.format(table_name=self.table2_name)
        try:
            self.cursor.execute(
                script,
                (tariff_data.tariff, tariff_data.price),
            )
        except OperationalError:
            print(config.DATABASE_CONNECTION_ERROR)

    def monthly_withdrawal(self, months: int):
        """
        Снятие денежных средств по тарифам у активных пользователей
        за указанное количество месяцев
        """
        # Поиск активных пользователей
        for month in range(1, months + 1):
            script = cmds.GET_ACTIVE_USERS.format(table_name=self.table_name)
            self.cursor.execute(script)
            active_users = self.cursor.fetchall()

            # Для каждого найденного пользователя
            for user in active_users:
                user_id, user_name, balance, tariff_ref = user
                script = cmds.GET_TARIFF_INFO.format(
                    table_name=self.table2_name
                )
                # По данным в поле tariff_ref смотрим, какой тариф
                self.cursor.execute(script, (tariff_ref,))
                tariff_info = self.cursor.fetchone()
                tariff, tariff_price = tariff_info

                # Если баланс пользователя позволяет оплатить тариф, оплачиваем
                if balance >= tariff_price:
                    new_balance = balance - tariff_price
                    script = cmds.UPDATE_USER_BALANCE.format(
                        table_name=self.table_name
                    )
                    self.cursor.execute(script, (new_balance, user_id))
                    print(
                        f'{user_name}, произведено снятие денежных средств '
                        f'в размере {tariff_price} по тарифу {tariff} '
                        f'за месяц №{month}'
                    )
                    # Если денежных средств недостаточно, меняем значение Activity
                else:
                    script = cmds.UPDATE_USER_ACTIVITY.format(
                        table_name=self.table_name
                    )
                    self.cursor.execute(script, (user_id,))
                    print(
                        f'{user_name}, у вас недостаточно средств на балансе.'
                    )
