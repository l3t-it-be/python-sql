from sqlite3 import OperationalError as SQLError


class ConfigStrings:

    AUTHORIZATION = '2. Авторизация'
    CHOOSE_ACTION = 'Выберите действие:'
    CURRENCY_EXCHANGE_SUCCESSFULLY_COMPLETED = 'Обмен валют успешно завершен'
    DATABASE_CONNECTION_ERROR = f'Ошибка подключения к базе данных: {SQLError}'
    EURO = 'EUR'
    EXIT = '4. Выход'
    FROM_CURRENCY = 'Какую валюту готовы предложить взамен? \n1. RUB\n2. USD\n3. EUR\n4. Выход из сервиса'
    GET_OPERATION = 'get'
    GIVE_OPERATION = 'give'
    GO_ON = 'п'

    INCORRECT_CHOICE = 'Неверный выбор. Пожалуйста, введите "Да" или "Нет".'
    INCORRECT_CHOICE_GO_ON_OR_LEAVE = (
        'Некорректный выбор. Пожалуйста, введите "П" или "В"'
    )
    INCORRECT_CODE = 'Неверный код восстановления'
    INCORRECT_CURRENCY = 'Неверная валюта'
    INCORRECT_CURRENCY_NUMBER = 'Неверный выбор номера валюты.'
    INCORRECT_NUMBER = 'Некорректное число'
    INCORRECT_PASSWORD = 'Неверный пароль'
    INPUT_CODE = 'Введите 4-х значный код для восстановления: '
    INPUT_CURRENCY_NUMBER = 'Введите номер валюты: '
    INPUT_LOGIN = 'Введите логин: '
    INPUT_NEW_PASSWORD = 'Введите новый пароль: '
    INPUT_NUMBER = 'Введите числовое значение'
    INPUT_OPERATION_NUMBER = 'Введите номер действия: '
    INPUT_PASSWORD = 'Введите пароль: '
    INPUT_YOUR_CODE = 'Введите ваш код для восстановления: '
    INVALID_CODE = 'Неверный код. Нужно ввести 4-х значное целое число.'

    LEAVE = 'в'
    LOGIN_ALREADY_EXISTS = 'Этот логин уже занят. Попробуйте другой.'
    LOGIN_AND_PASSWORD_SHOULD_NOT_BE_EMPTY = (
        'Логин и пароль не могут быть пустыми'
    )
    LOGIN_SHOULD_NOT_BE_NULL = 'Логин не может быть пустым'
    MSG_EXIT = 'Выход из программы'
    MSG_GOODBYE = 'До свидания!'
    NO = 'нет'
    NOT_ENOUGH_MONEY = 'Недостаточно средств на балансе'
    NOT_REGISTERED = 'Вы не зарегистрированы в нашей системе.\nПожалуйста, обратитесь в банк.'
    NULL_OR_NEGATIVE_SUM = (
        'Невозможно обменивать нулевую или отрицательную сумму'
    )

    OTHER_SUM_OR_LEAVE = 'Хотите ввести другую сумму или покинуть сервис? (П - Продолжить/В - Выйти): '
    PASSWORD_SHOULD_NOT_BE_NULL = 'Пароль не может быть пустым'
    PASSWORD_SUCCESSFULLY_CHANGED = 'Пароль успешно изменен'
    REGISTRATION = '1. Регистрация'
    RESET_PASSWORD = '3. Восстановление пароля'
    RUB = 'RUB'
    SAME_CURRENCY = 'Невозможно производить обмен двух одинаковых валют'
    SUCCESSFUL_REGISTRATION = (
        'Пользователь успешно зарегистрирован. Ваш логин: '
    )
    SUCCESSFULLY_AUTHORIZED = 'Вы успешно авторизованы'
    TO_CURRENCY = 'Введите какую валюту желаете получить: \n1. RUB\n2. USD\n3. EUR\n4. Выход из сервиса'

    USER_NOT_FOUND = 'Пользователь не найден'
    USD = 'USD'
    HOW_MUCH = 'Какая сумма Вас интересует?\n'
    WISH_TO_CONTINUE = 'Хотите продолжить? (Да/Нет): '
    WISH_TO_REGISTER = 'Хотите зарегистрироваться? (Да/Нет): '
    WISH_TO_RESET_PASSWORD = 'Хотите восстановить пароль? (Да/Нет): '
    YES = 'да'
