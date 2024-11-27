from mobile_app.sql_queries import MobileUsers, UserData, TariffData
from mobile_app.validations import validation


class Mobile:
    @staticmethod
    def mobile_logic():
        with MobileUsers() as mobile:
            mobile.create_tables()
            users = [
                UserData(user_name='User1', balance=10000, tariff_ref=2),
                UserData(user_name='User2', balance=10000, tariff_ref=3),
                UserData(user_name='User3', balance=10000, tariff_ref=1),
            ]
            for user in users:
                mobile.add_user(user)

            tariffs = [
                TariffData(tariff='Standard', price=500),
                TariffData(tariff='VIP', price=1000),
                TariffData(tariff='Premium', price=1500),
            ]
            for tariff in tariffs:
                mobile.add_tariff(tariff)

            months = validation.get_valid_months_input()
            mobile.monthly_withdrawal(months)


if __name__ == '__main__':
    start = Mobile()
    start.mobile_logic()
