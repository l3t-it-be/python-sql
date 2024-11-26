from atm_app.operations import Operation
from atm_app.sql_queries import SQLAtm, UserData
from config import ConfigStrings

config = ConfigStrings


class ATM:
    @staticmethod
    def atm_logic():
        with SQLAtm('atm_data') as atm:
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
                card_number = input(config.ENTER_YOUR_CARD)
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
                                    filename = config.FILE_FOR_REPORTS_1
                                    operation.report_operation(
                                        filename,
                                        card_number,
                                        current_operation,
                                        amount,
                                    )
                            elif current_operation == '4':
                                amount, card_number2 = data
                                if amount is False:
                                    print(
                                        config.OPERATION_CAN_NOT_BE_PERFORMED
                                    )
                                    continue
                                filename = config.FILE_FOR_REPORTS_1
                                operation.report_operation(
                                    filename,
                                    card_number,
                                    current_operation,
                                    amount,
                                )
                                if card_number2 is not None:
                                    filename = config.FILE_FOR_REPORTS_2
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
