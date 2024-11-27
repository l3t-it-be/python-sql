from config import config
from exchanger_app.enums import OperationChoice


class CurrenciesOperations:
    @staticmethod
    def get_currency_from_user(action: str) -> str:
        """Запрос валют, которые пользователь хочет обменять"""
        currency = None
        while True:
            if action == config.GET_OPERATION:
                print(config.TO_CURRENCY)
            elif action == config.GIVE_OPERATION:
                print(config.FROM_CURRENCY)

            currency_choice = input(config.INPUT_CURRENCY_NUMBER)
            if currency_choice == OperationChoice.RUB:
                currency = config.RUB
            elif currency_choice == OperationChoice.USD:
                currency = config.USD
            elif currency_choice == OperationChoice.EURO:
                currency = config.EURO
            elif currency_choice == OperationChoice.EXIT:
                print(config.MSG_GOODBYE)
                exit()
            else:
                print(config.INCORRECT_CURRENCY_NUMBER)
                continue

            if currency is not None:
                break

        return currency

    @staticmethod
    def get_money_amount() -> float:
        """Запрос денежной суммы, которую хочет получить пользователь"""
        while True:
            try:
                amount = float(input(config.HOW_MUCH))
                if amount <= 0:  # Проверка на отрицательную или нулевую сумму
                    print(config.NULL_OR_NEGATIVE_SUM)
                    continue
                else:
                    return amount
            except ValueError:
                print(config.INPUT_NUMBER)
                continue

    @staticmethod
    def make_choice() -> None:
        """Выбор действия при недостаточном балансе"""
        while True:
            choice = input(config.OTHER_SUM_OR_LEAVE).strip().lower()
            if choice == config.LEAVE:
                print(config.MSG_GOODBYE)
                exit()
            elif choice == config.GO_ON:
                break
            else:
                print(config.INCORRECT_CHOICE_GO_ON_OR_LEAVE)
