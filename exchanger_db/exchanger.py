from currencies_rates import Currencies
from operations import CurrenciesOperations
from sql_queries import DBManager


currencies = Currencies()
usd_to_rub, euro_to_rub, usd_to_euro, euro_to_usd = (
    currencies.get_exchange_rates()
)

print(
    'Добро пожаловать в наш обменный пункт, курс валют следующий:\n'
    f'1 USD = {usd_to_rub} RUB\n'
    f'1 EUR = {euro_to_rub} RUB\n'
    f'1 USD = {usd_to_euro} EUR\n'
    f'1 EUR = {euro_to_usd} USD'
)


class Exchanger:
    @staticmethod
    def exchanger_logic():
        db_manager = DBManager()
        db_manager.create_table()

        user_id = db_manager.add_user((100000, 1000, 1000))
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
        to_currency = operations.get_currency_from_user('get')
        while True:
            amount_to_receive = operations.get_money_amount()
            from_currency = operations.get_currency_from_user('give')
            enough_money = db_manager.check_balance(
                user_id,
                from_currency,
                to_currency,
                amount_to_receive,
                usd_to_rub,
                euro_to_rub,
                usd_to_euro,
                euro_to_usd,
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
                usd_to_rub,
                euro_to_rub,
                usd_to_euro,
                euro_to_usd,
            )
            break

        db_manager.show_balance(user_id)


if __name__ == '__main__':
    start = Exchanger()
    start.exchanger_logic()
