from currencies_rates import Currencies
from operations import CurrenciesOperations
from sql_queries import DBManager

from exchanger_db.currencies_rates import ExchangeRate


class Exchanger:
    @staticmethod
    def exchanger_logic(exchange: ExchangeRate):
        db_manager = DBManager()
        db_manager.create_table()

        user_id = db_manager.add_user((100000, 1000, 1000))
        user_in_system = db_manager.is_user_in_system(user_id)
        if not user_in_system:
            print(
                "Вы не зарегистрированы в нашей системе. "
                "Пожалуйста, обратитесь в банк."
            )
            return
        else:
            db_manager.show_balance(user_id)

        operations = CurrenciesOperations()
        to_currency = operations.get_currency_from_user("get")
        while True:
            amount_to_receive = operations.get_money_amount()
            from_currency = operations.get_currency_from_user("give")
            enough_money = db_manager.check_balance(
                user_id=user_id,
                from_currency=from_currency,
                to_currency=to_currency,
                amount_to_receive=amount_to_receive,
                exchange=exchange,
            )

            if from_currency == to_currency:
                print("Невозможно производить обмен двух одинаковых валют")
                continue
            elif not enough_money:
                print("Недостаточно средств на балансе")
                operations.make_choice()
                continue

            db_manager.exchange_currency(
                amount_to_receive,
                from_currency,
                to_currency,
                user_id,
                exchange,
            )
            break

        db_manager.show_balance(user_id)


def main():
    exchange = Currencies().get_exchange_rates()
    print(
        "Добро пожаловать в наш обменный пункт, курс валют следующий:\n"
        f"1 USD = {exchange.usd_to_rub} RUB\n"
        f"1 EUR = {exchange.euro_to_rub} RUB\n"
        f"1 USD = {exchange.usd_to_euro} EUR\n"
        f"1 EUR = {exchange.euro_to_usd} USD"
    )
    start = Exchanger()
    start.exchanger_logic(exchange)


if __name__ == "__main__":
    main()
