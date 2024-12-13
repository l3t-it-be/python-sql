from enum import StrEnum


class OperationChoice(StrEnum):
    """Варианты выбора ответа"""

    RUB = '1'
    USD = '2'
    EURO = '3'
    EXIT = '4'
