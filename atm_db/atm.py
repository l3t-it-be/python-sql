from atm_db.operations import Operation
from atm_db.sql_queries import SQLAtm, UserData


class ATM:
    @staticmethod
    def atm_logic():
        with SQLAtm() as atm:
            atm.create_table()
            user_data1 = UserData(
                card_number=1234, pin_code=1111, balance=10_000
            )
            user_data2 = UserData(
                card_number=2345, pin_code=2222, balance=10_000
            )
            atm.add_new_user(user_data1)
            atm.add_new_user(user_data2)

            while True:
                card_number = input('Пожалуйста, введите номер карты: ')
                if atm.insert_card(card_number):
                    if atm.input_code(card_number):
                        operation = Operation()
                        while True:
                            choice, data = operation.choose_operation(
                                card_number
                            )
                            current_operation = choice

                            if current_operation in ('2', '3'):
                                amount = data
                                if amount is not False:
                                    filename = 'report_1.csv'
                                    operation.report_operation(
                                        filename,
                                        card_number,
                                        current_operation,
                                        amount,
                                    )
                            elif current_operation == '4':
                                amount, card_number2 = data
                                if amount is False:
                                    print('Операция не может быть выполнена.')
                                    continue
                                filename = 'report_1.csv'
                                operation.report_operation(
                                    filename,
                                    card_number,
                                    current_operation,
                                    amount,
                                )
                                if card_number2 is not None:
                                    filename = 'report_2.csv'
                                    operation.report_operation(
                                        filename,
                                        card_number,
                                        current_operation,
                                        amount,
                                        card_number2,
                                    )
                    else:
                        break
                else:
                    break


if __name__ == '__main__':
    start = ATM()
    start.atm_logic()
