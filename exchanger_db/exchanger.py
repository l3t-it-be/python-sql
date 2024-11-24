from exchanger_db.currencies_rates import exchange_rate
from exchanger_db.operations import CurrenciesOperations
from exchanger_db.sql_queries import DBManager, UserBalance


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
                print(
                    'Вы не зарегистрированы в нашей системе. '
                    'Пожалуйста, обратитесь в банк.'
                )
                return
            else:
                db_manager.show_balance(user_id)

            operations = CurrenciesOperations()
            while True:
                to_currency = operations.get_currency_from_user('get')
                amount_to_receive = operations.get_money_amount()
                from_currency = operations.get_currency_from_user('give')

                enough_money = db_manager.check_balance(
                    user_id,
                    from_currency,
                    to_currency,
                    amount_to_receive,
                    exchange_rate,
                )

                if from_currency == to_currency:
                    print('Невозможно производить обмен двух одинаковых валют')
                    continue
                elif not enough_money:
                    print('Недостаточно средств на балансе')
                    operations.make_choice()
                    continue

                db_manager.exchange_currency(
                    amount_to_receive,
                    from_currency,
                    to_currency,
                    user_id,
                    exchange_rate,
                )
                break

            db_manager.show_balance(user_id)


def main():
    print(
        "Добро пожаловать в наш обменный пункт, курс валют следующий:\n"
        f"1 USD = {exchange_rate.usd_to_rub} RUB\n"
        f"1 EUR = {exchange_rate.euro_to_rub} RUB\n"
        f"1 USD = {exchange_rate.usd_to_euro} EUR\n"
        f"1 EUR = {exchange_rate.euro_to_usd} USD"
    )
    start = Exchanger()
    start.exchanger_logic()


if __name__ == "__main__":
    main()
