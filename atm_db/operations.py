import csv
import os
from datetime import datetime

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
                print('Выберите действие:')
                print('1. Узнать баланс')
                print('2. Снятие денежных средств')
                print('3. Внесение денежных средств')
                print('4. Перевести денежные средства')
                print('5. Завершить работу')

                choice = input('Введите номер операции: ')
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
                    print('До свидания! Всего вам доброго!')
                    exit()
                else:
                    print('Некорректный выбор операции')

    @staticmethod
    def create_csv(filename: str) -> None:
        """Создание файла для отчетов"""
        with open(filename, 'a', newline='') as csvfile:
            if filename == 'report_1.csv':
                data = [('Date', 'Card number', 'Operation type', 'Amount')]
            elif filename == 'report_2.csv':
                data = [
                    ('Date', 'Sender', 'Operation type', 'Amount', 'Payee')
                ]

            writer = csv.writer(csvfile, delimiter=';')
            writer.writerows(data)
        print(f'Создан файл {filename} для отчетов о финансовых операциях')

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
            print(
                'Операция не была выполнена. Запись в отчет не производится.'
            )
            return

        current_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        user_data = []

        if filename == 'report_1.csv':
            user_data = [
                (current_date, card_number1, current_operation, amount)
            ]
        elif filename == 'report_2.csv':
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

        print('Данные внесены в отчет')
