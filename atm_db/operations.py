from sql_queries import SQLAtm


class Operation:
    @staticmethod
    def choose_operation(card_number) -> None:
        atm = SQLAtm()
        while True:
            print('Выберите действие:')
            print('1. Узнать баланс')
            print('2. Снятие денежных средств')
            print('3. Внесение денежных средств')
            print('4. Завершить работу')

            choice = input('Введите номер операции: ')
            if choice == '1':
                atm.show_balance(card_number)
            elif choice == '2':
                atm.withdraw_money(card_number)
            elif choice == '3':
                atm.depositing_money(card_number)
            elif choice == '4':
                print('До свидания! Всего вам доброго!')
                exit()
            else:
                print('Некорректный выбор операции')
