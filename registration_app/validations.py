import re
from typing import Callable

from config import ConfigStrings

config = ConfigStrings()


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
    def login_password_are_not_empty(login, password) -> bool:
        if not login.strip() or not password.strip():
            print(config.LOGIN_AND_PASSWORD_SHOULD_NOT_BE_EMPTY)
            return False
        return True

    def check_login_not_null(self, login) -> bool:
        """Проверка того, что логин не пустой"""
        if not login.strip():
            print(config.LOGIN_SHOULD_NOT_BE_NULL)
            self.continue_or_not()
            return False
        return True

    def check_password_not_null(self, password) -> bool:
        """Проверка логина на корректность и уникальность"""
        if not password.strip():
            print(config.PASSWORD_SHOULD_NOT_BE_NULL)
            self.continue_or_not()
            return False
        return True

    @staticmethod
    def validate_code(code: str) -> bool:
        """Проверка соответствия переданного кода шаблону"""
        four_digits_pattern = re.compile(r'^\d{4}$')
        if not four_digits_pattern.match(code):
            print(config.INVALID_CODE)
            return False
        return True
