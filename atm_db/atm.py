from atm_db.operations import Operation
from atm_db.sql_queries import SQLAtm, UserData


class ATM:
    @staticmethod
    def atm_logic():
        with SQLAtm() as atm:
            atm.create_table()
            user_data = UserData(
                card_number=1234, pin_code=1111, balance=10_000
            )
            atm.add_new_user(user_data)

            while True:
                card_number = input('Пожалуйста, введите номер карты: ')
                if atm.insert_card(card_number):
                    if atm.input_code(card_number):
                        operation = Operation()
                        operation.choose_operation(card_number)
                    else:
                        break
                else:
                    break


if __name__ == '__main__':
    start = ATM()
    start.atm_logic()
