class CurrenciesOperations:
    """Запрос валют, которые пользователь хочет обменять"""

    @staticmethod
    def get_currency_from_user(action: str) -> str:
        currency = None
        while True:
            if action == 'get':
                print(
                    'Введите какую валюту желаете получить: \n'
                    '1. RUB\n'
                    '2. USD\n'
                    '3. EUR\n'
                    '4. Выход из сервиса'
                )
            elif action == 'give':
                print(
                    'Какую валюту готовы предложить взамен? \n'
                    '1. RUB\n'
                    '2. USD\n'
                    '3. EUR\n'
                    '4. Выход из сервиса'
                )

            currency_choice = input('Введите номер валюты: ')
            if currency_choice == '1':
                currency = 'RUB'
            elif currency_choice == '2':
                currency = 'USD'
            elif currency_choice == '3':
                currency = 'EUR'
            elif currency_choice == '4':
                print('До свидания!')
                exit()
            else:
                print('Неверный выбор номера валюты.')
                continue

            if currency is not None:
                break

        return currency

    """Запрос денежной суммы, которую хочет получить пользователь"""

    @staticmethod
    def get_money_amount() -> float:
        while True:
            try:
                amount = float(input('Какая сумма Вас интересует?\n'))
                if amount <= 0:  # Проверка на отрицательную или нулевую сумму
                    print(
                        'Невозможно обменивать нулевую или отрицательную сумму'
                    )
                    continue
                else:
                    return amount
            except ValueError:
                print('Введите числовое значение')
                continue

    """Выбор действия при недостаточном балансе"""

    @staticmethod
    def make_choice():
        while True:
            choice = (
                input(
                    'Хотите ввести другую сумму или покинуть сервис? (П - Продолжить/В - Выйти): '
                )
                .strip()
                .lower()
            )
            if choice == 'в':
                print('До свидания!')
                exit()
            elif choice == 'п':
                break
            else:
                print('Некорректный выбор. Пожалуйста, введите "П" или "В"')
