from datetime import datetime, timedelta

from mobile_calls_app.sql_queries import MobileCalls, UserData, MobilePrices


class CallsPrice:
    @staticmethod
    def mobile_calls_logic():
        with MobileCalls() as calls:
            calls.create_tables()
            user_id = calls.add_user(UserData(user='User1', balance=500))
            calls.add_prices(MobilePrices(mts_mts=1, mts_tele2=2, mts_yota=3))

            start_date = datetime.now()
            for i in range(30):
                current_date = start_date + timedelta(days=i)
                calls.perform_daily_call(user_id, date=current_date)


if __name__ == '__main__':
    start = CallsPrice()
    start.mobile_calls_logic()
