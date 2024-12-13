from config import config
from exchanger_app.currencies_rates import exchange_rates
from exchanger_app.operations import CurrenciesOperations
from exchanger_app.sql_queries import DBManager, UserBalance


class Exchanger:
    @staticmethod
    def exchanger_logic():
        with DBManager() as db_manager:
            db_manager.create_table()
            user_balance = UserBalance(
                balance_rub=100_000, balance_usd=1000, balance_euro=1000
            )
            user_id = db_manager.add_user(user_balance)
            user_in_system = db_manager.is_user_in_system(user_id)
            if not user_in_system:
                print(config.NOT_REGISTERED)
                return
            else:
                db_manager.show_balance(user_id)

            operations = CurrenciesOperations()
            while True:
                to_currency = operations.get_currency_from_user(
                    config.GET_OPERATION
                )
                amount_to_receive = operations.get_money_amount()
                from_currency = operations.get_currency_from_user(
                    config.GIVE_OPERATION
                )

                enough_money = db_manager.check_balance(
                    user_id,
                    from_currency,
                    to_currency,
                    amount_to_receive,
                    exchange_rates,
                )

                if from_currency == to_currency:
                    print(config.SAME_CURRENCY)
                    continue
                elif not enough_money:
                    print(config.NOT_ENOUGH_MONEY)
                    operations.make_choice()
                    continue

                db_manager.exchange_currency(
                    amount_to_receive,
                    from_currency,
                    to_currency,
                    user_id,
                    exchange_rates,
                )
                break

            db_manager.show_balance(user_id)


def main():
    print(
        "Добро пожаловать в наш обменный пункт, курс валют следующий:\n"
        f"1 USD = {exchange_rates.usd_to_rub} RUB\n"
        f"1 EUR = {exchange_rates.euro_to_rub} RUB\n"
        f"1 USD = {exchange_rates.usd_to_euro} EUR\n"
        f"1 EUR = {exchange_rates.euro_to_usd} USD"
    )
    start = Exchanger()
    start.exchanger_logic()


if __name__ == '__main__':
    main()
