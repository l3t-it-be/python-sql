from dataclasses import dataclass
from sqlite3 import OperationalError

from atm_app import cmds
from config import config
from initialize_bd import Initialization


@dataclass(kw_only=True)
class UserData:
    card_number: int
    pin_code: int
    balance: int


class SQLAtm(Initialization):
    def __init__(self):
        super().__init__('atm_data')

    def create_table(self) -> None:
        """Создание таблицы"""
        script = cmds.CREATE_TABLE_USERS_DATA.format(
            table_name=self.table_name
        )
        try:
            self.cursor.execute(script)
        except OperationalError:
            print(config.DATABASE_CONNECTION_ERROR)

    def add_new_user(self, users_data: UserData) -> None:
        """Добавление в таблицу пользователя (если такого еще нет)"""
        script = cmds.SELECT_CARD_NUMBER_IF_EXISTS.format(
            table_name=self.table_name
        )
        self.cursor.execute(script, (users_data.card_number,))

        user = self.cursor.fetchone()
        if user is None:
            script = cmds.INSERT_USERS_DATA.format(table_name=self.table_name)
            try:
                self.cursor.execute(
                    script,
                    (
                        users_data.card_number,
                        users_data.pin_code,
                        users_data.balance,
                    ),
                )
            except OperationalError:
                print(config.DATABASE_CONNECTION_ERROR)
            else:
                print(config.CARD_NUMBER_ALREADY_REGISTERED)

    def check_result(self, card_number: str) -> bool:
        """Проверка номера введенной карты"""
        result = self.cursor.fetchone()
        if result is None:
            print(config.UNKNOWN_CARD_NUMBER)
            return False

        if result[1] == 1:
            print(config.CARD_BLOCKED)
            return False

        print(config.CARD_ENTERED, card_number)
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
            pin_code = input(config.MSG_ENTER_PIN_CODE)
            script = cmds.SELECT_PIN_CODE.format(table_name=self.table_name)
            self.cursor.execute(script, (card_number,))

            result = self.cursor.fetchone()
            try:
                if int(pin_code) == result[0]:
                    print(config.CORRECT_PIN_CODE_ENTERED)
                    return True
                else:
                    attempts -= 1
                    print(config.INCORRECT_PIN_CODE, attempts)
            except ValueError:
                attempts -= 1
                print(config.INCORRECT_PIN_CODE, attempts)

        # Блокировка карты после трех неудачных попыток
        script = cmds.BLOCK_CARD_NUMBER.format(table_name=self.table_name)
        try:
            self.cursor.execute(script, (card_number,))
        except OperationalError:
            print(config.DATABASE_CONNECTION_ERROR)
        print(config.CARD_BLOCKED)
        return False

    def show_balance(self, card_number: str) -> None:
        """Вывод баланса карты"""
        script = cmds.SHOW_BALANCE.format(table_name=self.table_name)
        self.cursor.execute(script, (card_number,))

        result = self.cursor.fetchone()
        if result is not None:
            print(config.BALANCE_MSG, f'{result[0]} руб.')
        else:
            print(config.CARD_NOT_FOUND)

    def withdraw_money(self, card_number: str) -> bool | str:
        """Снятие денежных средств с карты"""
        while True:
            try:
                amount = input(config.ENTER_SUM_TO_WITHDRAW)
                if int(amount) <= 0:
                    print(config.INCORRECT_SUM_OF_MONEY)
                    continue
                else:
                    break
            except ValueError:
                print(config.INCORRECT_VALUE)
                return False

        script = cmds.SHOW_BALANCE.format(table_name=self.table_name)
        self.cursor.execute(script, (card_number,))

        result = self.cursor.fetchone()

        if int(amount) > result[0]:
            print(config.NOT_ENOUGH_MONEY)
            return False
        else:
            script = cmds.REDUCE_BALANCE.format(
                table_name=self.table_name, amount=amount
            )
            try:
                self.cursor.execute(script, (card_number,))
            except OperationalError:
                print(config.DATABASE_CONNECTION_ERROR)

        self.show_balance(card_number)
        return amount

    def depositing_money(self, card_number: str) -> bool | str:
        """Внесение денежных средств на карту"""
        while True:
            try:
                amount = input(config.ENTER_SUM_TO_DEPOSIT)
                if int(amount) <= 0:
                    print(config.INCORRECT_SUM_OF_MONEY)
                    continue
                else:
                    break
            except ValueError:
                print(config.INCORRECT_VALUE)
                return False

        script = cmds.INCREASE_BALANCE.format(
            table_name=self.table_name, amount=amount
        )
        try:
            self.cursor.execute(script, (card_number,))
        except OperationalError:
            print(config.DATABASE_CONNECTION_ERROR)

        self.show_balance(card_number)
        return amount

    def transfer_money(
        self, card_number: str
    ) -> tuple[bool, None] | tuple[str, str]:
        """Перевод денежных средств между клиентами"""
        recipient_card_number = input(config.ENTER_PAYEE_CARD)

        if card_number == recipient_card_number:
            print(config.SAME_CARD)
            return False, None

        script = cmds.SELECT_CARD_NUMBER_AND_IsBlocked.format(
            table_name=self.table_name
        )
        self.cursor.execute(script, (recipient_card_number,))

        result = self.cursor.fetchone()
        if result is None:
            print(config.PAYEE_CARD_NOT_FOUND)
            return False, None

        if result[1] == 1:
            print(config.PAYEE_CARD_BLOCKED)
            return False, None

        while True:
            try:
                amount = input(config.ENTER_SUM_TO_TRANSFER)
                if int(amount) <= 0:
                    print(config.INCORRECT_SUM_OF_MONEY)
                    continue
                else:
                    break
            except ValueError:
                print(config.INCORRECT_VALUE)
                return False, None

        script = cmds.SHOW_BALANCE.format(table_name=self.table_name)
        self.cursor.execute(script, (card_number,))

        result = self.cursor.fetchone()

        if int(amount) > result[0]:
            print(config.NOT_ENOUGH_MONEY)
            return False, None
        else:
            try:
                # Списание денежных средств с карты отправителя
                script = cmds.REDUCE_BALANCE.format(
                    table_name=self.table_name, amount=amount
                )
                self.cursor.execute(script, (card_number,))

                # Зачисление денежных средств на карту получателя
                script = cmds.INCREASE_BALANCE.format(
                    table_name=self.table_name, amount=amount
                )
                self.cursor.execute(script, (recipient_card_number,))
            except OperationalError:
                print(config.DATABASE_CONNECTION_ERROR)
                return False, None

        self.show_balance(card_number)
        return amount, recipient_card_number
