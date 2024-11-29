from atm_app.operations import Operation
from atm_app.reports import Report
from atm_app.sql_queries import SQLAtm, UserData
from config import config

report = Report()


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
                card_number = input(config.ENTER_YOUR_CARD)
                if not atm.insert_card(card_number):
                    break
                if not atm.input_code(card_number):
                    break

                operation = Operation()
                while True:
                    choice, data = operation.choose_operation(card_number)

                    if choice in ('2', '3'):
                        amount = data
                        if amount is not False:
                            report.report_operation(
                                config.FILE_FOR_REPORTS_1,
                                card_number,
                                choice,
                                amount,
                            )
                    elif choice == '4':
                        amount, card_number2 = data
                        if amount is False:
                            print(config.OPERATION_CAN_NOT_BE_PERFORMED)
                            continue
                        report.report_operation(
                            config.FILE_FOR_REPORTS_1,
                            card_number,
                            choice,
                            amount,
                        )
                        if card_number2 is not None:
                            report.report_operation(
                                config.FILE_FOR_REPORTS_2,
                                card_number,
                                choice,
                                amount,
                                card_number2,
                            )


if __name__ == '__main__':
    start = ATM()
    start.atm_logic()
