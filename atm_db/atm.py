from operations import Operation
from sql_queries import SQLAtm


class ATM:
    @staticmethod
    def atm_logic():
        with SQLAtm() as atm:
            atm.create_table()
            atm.add_new_user((1234, 1111, 10_000))

            while True:
                card_number = input("Пожалуйста, введите номер карты: ")
                if atm.insert_card(card_number):
                    if atm.input_code(card_number):
                        operation = Operation()
                        operation.choose_operation(card_number)
                    else:
                        continue
                else:
                    continue


if __name__ == "__main__":
    start = ATM()
    start.atm_logic()
