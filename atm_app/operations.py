import csv
import os
from datetime import datetime

from config import config
from sql_queries import SQLAtm
from enums import OperationChoice


class Operation:
    @staticmethod
    def choose_operation(
        card_number: str,
    ) -> (
        tuple[str, None]
        | tuple[str, bool | str]
        | tuple[str, tuple[bool, None] | tuple[str, str]]
    ):
        """Выбор операции"""
        with SQLAtm() as atm:
            while True:
                print(config.CHOOSE_ACTION)
                print(config.SHOW_BALANCE_1)
                print(config.WITHDRAW_MONEY_2)
                print(config.DEPOSITING_MONEY_3)
                print(config.TRANSFER_MONEY_4)
                print(config.EXIT_5)

                choice = input(config.INPUT_OPERATION_NUMBER)
                if choice == OperationChoice.SHOW_BALANCE:
                    atm.show_balance(card_number)
                    return choice, None
                elif choice == OperationChoice.WITHDRAW_MONEY:
                    data = atm.withdraw_money(card_number)
                    return choice, data
                elif choice == OperationChoice.DEPOSITING_MONEY:
                    data = atm.depositing_money(card_number)
                    return choice, data
                elif choice == OperationChoice.TRANSFER_MONEY:
                    data = atm.transfer_money(card_number)
                    return choice, data
                elif choice == OperationChoice.EXIT:
                    print(config.MSG_GOODBYE)
                    exit()
                else:
                    print(config.INCORRECT_OPERATION_CHOICE)

    @staticmethod
    def create_csv(filename: str) -> None:
        """Создание файла для отчетов"""
        with open(filename, 'a', newline='') as csvfile:
            if filename == config.FILE_FOR_REPORTS_1:
                data = config.DATA_FOR_REPORTS_1
            elif filename == config.FILE_FOR_REPORTS_2:
                data = config.DATA_FOR_REPORTS_2

            writer = csv.writer(csvfile, delimiter=';')
            writer.writerows(data)
        print(config.FILE_FOR_REPORTS_CREATED, filename)

    def report_operation(
        self,
        filename,
        card_number1: str,
        current_operation: str,
        amount: str,
        card_number2=None,
    ) -> None:
        """Запись данных в файл для отчета"""
        if amount is False:
            print(config.OPERATION_WAS_NOT_PERFORMED)
            return

        current_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        user_data = []

        if filename == config.FILE_FOR_REPORTS_1:
            user_data = [
                (current_date, card_number1, current_operation, amount)
            ]
        elif filename == config.FILE_FOR_REPORTS_2:
            user_data = [
                (
                    current_date,
                    card_number1,
                    current_operation,
                    amount,
                    card_number2,
                )
            ]

        # Проверка существования файла и его создание, если он не существует
        if not os.path.exists(filename):
            self.create_csv(filename)

        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerows(user_data)

        print(config.DATA_REPORTED, filename)
