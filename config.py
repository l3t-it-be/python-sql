from sqlite3 import OperationalError as SQLError


class ConfigStrings:
    AUTHORIZATION_2 = '2. Авторизация'
    BALANCE_MSG = 'Баланс вашей карты:'
    CARD_BLOCKED = 'Карта заблокирована'
    CARD_ENTERED = 'Введена карта с номером'
    CARD_NOT_FOUND = 'Карта не найдена'
    CARD_NUMBER_ALREADY_REGISTERED = (
        'Пользователь с таким номером карты уже зарегистрирован в системе'
    )
    CHOOSE_ACTION = 'Выберите действие:'
    CONNECTION_PROBLEMS = 'Временные неполадки в сети'
    CORRECT_PIN_CODE_ENTERED = 'Введен верный пин-код'
    CURRENCY_EXCHANGE_SUCCESSFULLY_COMPLETED = 'Обмен валют успешно завершен'
    DATA_FOR_MOBILE_REPORTS = [('Date', 'Operator', 'Count_min', 'Amount')]
    DATA_FOR_REPORTS_1 = [('Date', 'Card number', 'Operation type', 'Amount')]
    DATA_FOR_REPORTS_2 = [
        ('Date', 'Sender', 'Operation type', 'Amount', 'Payee')
    ]
    DATA_REPORTED = 'Данные внесены в отчет'
    DATABASE_CONNECTION_ERROR = f'Ошибка подключения к базе данных: {SQLError}'
    DEPOSITING_MONEY_3 = '3. Внесение денежных средств'
    ENTER_PAYEE_CARD = 'Введите номер карты получателя: '
    ENTER_SUM_TO_DEPOSIT = 'Введите сумму, которую желаете внести: '
    ENTER_SUM_TO_TRANSFER = 'Введите сумму, которую желаете перевести: '
    ENTER_SUM_TO_WITHDRAW = 'Введите сумму, которую желаете снять: '
    ENTER_YOUR_CARD = 'Пожалуйста, введите номер карты: '
    EURO = 'EUR'
    EXIT_4 = '4. Выход'
    EXIT_5 = '5. Завершить работу'
    FILE_FOR_MOBILE_REPORTS = 'report_mobile.csv'
    FILE_FOR_REPORTS_1 = 'report_1.csv'
    FILE_FOR_REPORTS_2 = 'report_2.csv'
    FILE_FOR_MOBILE_REPORTS_CREATED = (
        'Создан файл "report_mobile.csv" для отчетов о совершенных звонках'
    )
    FILE_FOR_REPORTS_CREATED = 'Создан файл для отчетов о финансовых операциях'
    FROM_CURRENCY = (
        'Какую валюту готовы предложить взамен? '
        '\n1. RUB\n2. USD\n3. EUR\n4. Выход из сервиса'
    )
    GET_OPERATION = 'get'
    GIVE_OPERATION = 'give'
    GO_ON = 'п'
    HOW_MUCH = 'Какая сумма Вас интересует?\n'
    INCORRECT_CHOICE = 'Неверный выбор. Пожалуйста, введите "Да" или "Нет".'
    INCORRECT_CHOICE_GO_ON_OR_LEAVE = (
        'Некорректный выбор. Пожалуйста, введите "П" или "В".'
    )
    INCORRECT_CODE = 'Неверный код восстановления'
    INCORRECT_CURRENCY = 'Неверная валюта'
    INCORRECT_CURRENCY_NUMBER = 'Неверный выбор номера валюты'
    INCORRECT_NUMBER = 'Некорректное число'
    INCORRECT_OPERATION_CHOICE = 'Некорректный выбор операции'
    INCORRECT_PASSWORD = 'Неверный пароль'
    INCORRECT_PIN_CODE = 'Неверный пин-код. Осталось попыток:'
    INCORRECT_SUM_OF_MONEY = 'Некорректное значение суммы денежных средств'
    INCORRECT_VALUE = 'Некорректное значение'
    INPUT_CODE = 'Введите 4-х значный код для восстановления: '
    INPUT_CURRENCY_NUMBER = 'Введите номер валюты: '
    INPUT_LOGIN = 'Введите логин: '
    INPUT_MONTHS_QUANTITY = 'Введите период расчета в месяцах (целое число): '
    INPUT_NEW_PASSWORD = 'Введите новый пароль: '
    INPUT_NUMBER = 'Введите числовое значение'
    INPUT_NUMBER_OF_ACTION = 'Введите номер действия: '
    INPUT_OPERATION_NUMBER = 'Введите номер операции: '
    INPUT_PASSWORD = 'Введите пароль: '
    INPUT_YOUR_CODE = 'Введите ваш код для восстановления: '
    INVALID_CODE = 'Неверный код. Нужно ввести 4-х значное целое число.'
    LEAVE = 'в'
    LOGIN_ALREADY_EXISTS = 'Этот логин уже занят. Попробуйте другой.'
    LOGIN_AND_PASSWORD_SHOULD_NOT_BE_EMPTY = (
        'Логин и пароль не могут быть пустыми'
    )
    LOGIN_SHOULD_NOT_BE_NULL = 'Логин не может быть пустым'
    MINUTES = 'мин'
    MSG_ENTER_PIN_CODE = 'Введите пин-код: '
    MSG_EXIT = 'Выход из программы'
    MSG_GOODBYE = 'До свидания! Всего вам доброго!'
    MOBILE_OPERATORS = ['Mts_Mts', 'Mts_Tele2', 'Mts_Yota']
    NO = 'нет'
    NOT_ENOUGH_MONEY = 'На вашей карте недостаточно денежных средств'
    NOT_ENOUGH_MONEY_ON_BALANCE = (
        'Недостаточно средств на балансе для осуществления звонка'
    )
    NOT_REGISTERED = (
        'Вы не зарегистрированы в нашей системе.\n'
        'Пожалуйста, обратитесь в банк.'
    )
    NULL_OR_NEGATIVE_SUM = (
        'Невозможно обменивать нулевую или отрицательную сумму'
    )
    OPERATION_CAN_NOT_BE_PERFORMED = 'Операция не может быть выполнена'
    OPERATION_WAS_NOT_PERFORMED = (
        'Операция не была выполнена. ' 'Запись в отчет не производится.'
    )
    OTHER_SUM_OR_LEAVE = (
        'Хотите ввести другую сумму или покинуть сервис? '
        '(П - Продолжить/В - Выйти): '
    )
    PASSWORD_SHOULD_NOT_BE_NULL = 'Пароль не может быть пустым'
    PASSWORD_SUCCESSFULLY_CHANGED = 'Пароль успешно изменен'
    PAYEE_CARD_BLOCKED = 'Карта получателя заблокирована'
    PAYEE_CARD_NOT_FOUND = 'Карта получателя не найдена'
    PRICES_ALREADY_ADDED = 'Цены уже добавлены в таблицу'
    REGISTRATION_1 = '1. Регистрация'
    RESET_PASSWORD_3 = '3. Восстановление пароля'
    RUB = 'RUB'
    RUB_RUS = 'руб'
    SAME_CARD = (
        'Вы указали номер собственной карты.\n'
        'Невозможно переводить денежные средства самому себе.'
    )
    SAME_CURRENCY = 'Невозможно производить обмен двух одинаковых валют'
    SHOW_BALANCE_1 = '1. Узнать баланс'
    SUCCESSFUL_CALL = 'Звонок завершен'
    SUCCESSFUL_REGISTRATION = 'Пользователь успешно зарегистрирован. Логин:'
    SUCCESSFULLY_AUTHORIZED = 'Вы успешно авторизованы'
    TARIFF_ALREADY_EXISTS = 'Тариф с таким названием уже добавлен в систему'
    TO_CURRENCY = (
        'Введите какую валюту желаете получить: '
        '\n1. RUB\n2. USD\n3. EUR\n4. Выход из сервиса'
    )
    TRANSFER_MONEY_4 = '4. Перевести денежные средства'
    UNKNOWN_CARD_NUMBER = (
        'Введен неизвестный номер карты. Пожалуйста, обратитесь в банк.'
    )
    USER_ALREADY_EXISTS = 'Пользователь c таким именем уже добавлен в систему'
    USER_NOT_FOUND = 'Пользователь не найден'
    USD = 'USD'
    WITHDRAW_MONEY_2 = '2. Снятие денежных средств'
    WISH_TO_CONTINUE = 'Хотите продолжить? (Да/Нет): '
    WISH_TO_REGISTER = 'Хотите зарегистрироваться? (Да/Нет): '
    WISH_TO_RESET_PASSWORD = 'Хотите восстановить пароль? (Да/Нет): '
    YES = 'да'


config = ConfigStrings()
