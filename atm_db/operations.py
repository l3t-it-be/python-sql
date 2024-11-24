from sql_queries import SQLAtm
from enums import OperationChoice


class Operation:
    @staticmethod
    def choose_operation(card_number: str) -> None:
        with SQLAtm() as atm:
            while True:
                print('Выберите действие:')
                print('1. Узнать баланс')
                print('2. Снятие денежных средств')
                print('3. Внесение денежных средств')
                print('4. Завершить работу')

                choice = input('Введите номер операции: ')
                if choice == OperationChoice.SHOW_BALANCE:
                    atm.show_balance(card_number)
                elif choice == OperationChoice.WITHDRAW_MONEY:
                    atm.withdraw_money(card_number)
                elif choice == OperationChoice.DEPOSITING_MONEY:
                    atm.depositing_money(card_number)
                elif choice == OperationChoice.EXIT:
                    print('До свидания! Всего вам доброго!')
                    exit()
                else:
                    print('Некорректный выбор операции')
