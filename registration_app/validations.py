import re
from typing import Callable

from config import config


def error_logger(msg: str):
    def wrapper(func: Callable):
        def wrapped(*args, **kwargs) -> bool:
            """Получение результата проверки True | False"""
            result = func(*args, **kwargs)
            if not result:
                print(msg)  # Если проверка не прошла - вывести сообщение
            return result

        return wrapped

    return wrapper


class Validation:
    @staticmethod
    def continue_or_not() -> None:
        while True:
            choice = input(config.WISH_TO_CONTINUE).strip().lower()
            if choice == config.YES:
                break
            elif choice == config.NO:
                print(config.MSG_EXIT)
                exit()
            else:
                print(config.INCORRECT_CHOICE)
            continue

    @staticmethod
    def register_or_not(func: Callable) -> None:
        while True:
            choice = input(config.WISH_TO_REGISTER).strip().lower()
            if choice == config.YES:
                func()
                break
            elif choice == config.NO:
                print(config.MSG_EXIT)
                exit()
            else:
                print(config.INCORRECT_CHOICE)
                continue

    @staticmethod
    def reset_password_or_not(func: Callable) -> None:
        while True:
            choice = input(config.WISH_TO_RESET_PASSWORD).strip().lower()
            if choice == config.YES:
                func()
                break
            elif choice == config.NO:
                print(config.MSG_EXIT)
                exit()
            else:
                print(config.INCORRECT_CHOICE)
                continue

    @staticmethod
    @error_logger(msg=config.LOGIN_AND_PASSWORD_SHOULD_NOT_BE_EMPTY)
    def login_password_are_not_empty(login, password) -> bool:
        return login.strip() and password.strip()

    @error_logger(msg=config.LOGIN_SHOULD_NOT_BE_NULL)
    def check_login_not_null(self, login) -> bool:
        """Проверка того, что логин не пустой"""
        return bool(login.strip())

    @error_logger(msg=config.PASSWORD_SHOULD_NOT_BE_NULL)
    def check_password_not_null(self, password) -> bool:
        """Проверка логина на корректность и уникальность"""
        return bool(password.strip())

    @staticmethod
    @error_logger(msg=config.INVALID_CODE)
    def validate_code(code: str) -> bool:
        """Проверка соответствия переданного кода шаблону"""
        four_digits_pattern = re.compile(r'^\d{4}$')
        return bool(four_digits_pattern.match(code))


validation = Validation()
