from sqlite3 import OperationalError as SQLError


class ConfigStrings:

    AUTHORIZATION = '2. Авторизация'
    CHOOSE_ACTION = 'Выберите действие:'
    EXIT = '4. Выход'
    DATABASE_CONNECTION_ERROR = f'Ошибка подключения к базе данных: {SQLError}'

    INCORRECT_CHOICE = 'Неверный выбор. Пожалуйста, введите "Да" или "Нет".'
    INCORRECT_CODE = 'Неверный код восстановления'
    INCORRECT_NUMBER = 'Некорректное число'
    INCORRECT_PASSWORD = 'Неверный пароль'
    INPUT_CODE = 'Введите 4-х значный код для восстановления: '
    INPUT_LOGIN = 'Введите логин: '
    INPUT_NEW_PASSWORD = 'Введите новый пароль: '
    INPUT_NUMBER = 'Введите номер действия: '
    INPUT_PASSWORD = 'Введите пароль: '
    INPUT_YOUR_CODE = 'Введите ваш код для восстановления: '
    INVALID_CODE = 'Неверный код. Нужно ввести 4-х значное целое число.'

    LOGIN_ALREADY_EXISTS = 'Этот логин уже занят. Попробуйте другой.'
    LOGIN_AND_PASSWORD_SHOULD_NOT_BE_EMPTY = (
        'Логин и пароль не могут быть пустыми'
    )
    LOGIN_SHOULD_NOT_BE_NULL = 'Логин не может быть пустым'
    MSG_EXIT = 'Выход из программы'
    NO = 'нет'

    PASSWORD_SHOULD_NOT_BE_NULL = 'Пароль не может быть пустым'
    PASSWORD_SUCCESSFULLY_CHANGED = 'Пароль успешно изменен'
    REGISTRATION = '1. Регистрация'
    RESET_PASSWORD = '3. Восстановление пароля'
    SUCCESSFUL_REGISTRATION = (
        'Пользователь успешно зарегистрирован. Ваш логин: '
    )
    SUCCESSFULLY_AUTHORIZED = 'Вы успешно авторизованы'

    USER_NOT_FOUND = 'Пользователь не найден'
    WISH_TO_CONTINUE = 'Хотите продолжить? (Да/Нет): '
    WISH_TO_REGISTER = 'Хотите зарегистрироваться? (Да/Нет): '
    WISH_TO_RESET_PASSWORD = 'Хотите восстановить пароль? (Да/Нет): '
    YES = 'да'
