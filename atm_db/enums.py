from enum import StrEnum


class OperationChoice(StrEnum):
    """Варианты выбора ответа"""

    SHOW_BALANCE = '1'
    WITHDRAW_MONEY = '2'
    DEPOSITING_MONEY = '3'
    TRANSFER_MONEY = '4'
    EXIT = '5'
