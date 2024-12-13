from config import config
from sql_queries import SQLAtm
from enums import OperationChoice


class Operation:
    OperationType = (
        tuple[str, None]
        | tuple[str, bool | str]
        | tuple[str, tuple[bool, None] | tuple[str, str]]
        | None
    )

    @staticmethod
    def choose_operation(card_number: str) -> OperationType:
        """Выбор операции"""
        with SQLAtm() as atm:
            while True:
                print(
                    config.CHOOSE_ACTION,
                    config.SHOW_BALANCE_1,
                    config.WITHDRAW_MONEY_2,
                    config.DEPOSITING_MONEY_3,
                    config.TRANSFER_MONEY_4,
                    config.EXIT_5,
                    sep='\n',
                )

                choice = input(config.INPUT_OPERATION_NUMBER)
                if choice == OperationChoice.SHOW_BALANCE:
                    atm.show_balance(card_number)
                    return choice, None
                if choice == OperationChoice.WITHDRAW_MONEY:
                    data = atm.withdraw_money(card_number)
                    return choice, data
                if choice == OperationChoice.DEPOSITING_MONEY:
                    data = atm.depositing_money(card_number)
                    return choice, data
                if choice == OperationChoice.TRANSFER_MONEY:
                    data = atm.transfer_money(card_number)
                    return choice, data
                if choice == OperationChoice.EXIT:
                    print(config.MSG_GOODBYE)
                    exit()
                else:
                    print(config.INCORRECT_OPERATION_CHOICE)
