from exchanger_db.enums import OperationChoice


class CurrenciesOperations:
    @staticmethod
    def get_currency_from_user(action: str) -> str:
        """Запрос валют, которые пользователь хочет обменять"""
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
            if currency_choice == OperationChoice.RUB:
                currency = 'RUB'
            elif currency_choice == OperationChoice.USD:
                currency = 'USD'
            elif currency_choice == OperationChoice.EURO:
                currency = 'EUR'
            elif currency_choice == OperationChoice.EXIT:
                print('До свидания!')
                exit()
            else:
                print('Неверный выбор номера валюты.')
                continue

            if currency is not None:
                break

        return currency

    @staticmethod
    def get_money_amount() -> float:
        """Запрос денежной суммы, которую хочет получить пользователь"""
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

    @staticmethod
    def make_choice() -> None:
        """Выбор действия при недостаточном балансе"""
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
