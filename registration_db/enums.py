from enum import StrEnum


class OperationChoice(StrEnum):
    """Варианты выбора ответа"""

    REGISTER_NEW_USER = '1'
    AUTHORIZE_USER = '2'
    RESET_PASSWORD = '3'
    EXIT = '4'
