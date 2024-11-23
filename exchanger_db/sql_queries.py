import sqlite3
from typing import Tuple

from selene.common.data_structures.persistent import dataclass

from exchanger_db.currencies_rates import ExchangeRate


@dataclass
class Balance:
    rub: float
    usd: float
    eur: float

    def __str__(self) -> str:
        return (
            f"Ваш баланс: \n"
            f"RUB - {self.rub:.2f}\n"
            f"USD - {self.usd:.2f}\n"
            f"EUR - {self.eur:.2f}"
        )


class DBManager:
    def __init__(self):
        self.db_name = "exchanger.db"
        self.table_name = "users_balance"

    """Создание таблицы"""

    def create_table(self) -> None:
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute(
                f"""CREATE TABLE IF NOT EXISTS {self.table_name}
                    (
                        UserID INTEGER PRIMARY KEY,
                        Balance_RUB FLOAT NOT NULL,
                        Balance_USD FLOAT,
                        Balance_EUR FLOAT
                    );
                    """
            )

    """Добавление в таблицу пользователя"""

    def add_user(self, user_balance: Tuple[int, int, int]) -> int:
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute(
                f"""INSERT INTO {self.table_name}
                            (Balance_RUB, Balance_USD, Balance_EUR) 
                        VALUES (?, ?, ?);""",
                user_balance,
            )
            user_id = cur.lastrowid
            print(f"Пользователь {user_id} успешно зарегистрирован")
            return user_id

    """Проверка того, что пользователь зарегистрирован в системе"""

    def is_user_in_system(self, user_id: int) -> bool:
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute(
                f"""SELECT * FROM {self.table_name} 
                        WHERE UserID = ?;""",
                (user_id,),
            )
            user = cur.fetchone()
            return bool(user)

    """Вывод баланса"""

    def show_balance(self, user_id: int) -> None:
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute(
                f"""SELECT Balance_RUB, Balance_USD, Balance_EUR
                        FROM {self.table_name}
                        WHERE UserID = ?;
                    """,
                (user_id,),
            )
            balance = cur.fetchone()
            if not balance:
                print("Нет данных в БД")
                return

            print(Balance(*balance))

    """Проверка баланса"""

    def check_balance(
        self,
        user_id: int,
        from_currency: str,
        to_currency: str,
        amount_to_receive: float,
        exchange: ExchangeRate,
    ) -> bool:
        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()
            cur.execute(
                f"""SELECT Balance_RUB, Balance_USD, Balance_EUR
                        FROM {self.table_name}
                        WHERE UserID = ?;
                    """,
                (user_id,),
            )
            balance = cur.fetchone()

            if from_currency == "RUB":
                if to_currency == "USD":
                    amount_to_withdraw = round(
                        amount_to_receive * exchange.usd_to_rub, 2
                    )
                    return (
                        balance[0] >= amount_to_withdraw
                        and balance[1] >= amount_to_receive
                    )
                elif to_currency == "EUR":
                    amount_to_withdraw = round(
                        amount_to_receive * exchange.euro_to_rub, 2
                    )
                    return (
                        balance[0] >= amount_to_withdraw
                        and balance[2] >= amount_to_receive
                    )
            elif from_currency == "USD":
                if to_currency == "RUB":
                    amount_to_withdraw = round(
                        amount_to_receive / exchange.usd_to_rub, 2
                    )
                    return (
                        balance[1] >= amount_to_withdraw
                        and balance[0] >= amount_to_receive
                    )
                elif to_currency == "EUR":
                    amount_to_withdraw = round(
                        amount_to_receive * exchange.usd_to_euro, 2
                    )
                    return (
                        balance[1] >= amount_to_withdraw
                        and balance[2] >= amount_to_receive
                    )
            elif from_currency == "EUR":
                if to_currency == "RUB":
                    amount_to_withdraw = round(
                        amount_to_receive / exchange.euro_to_rub, 2
                    )
                    return (
                        balance[2] >= amount_to_withdraw
                        and balance[0] >= amount_to_receive
                    )
                elif to_currency == "USD":
                    amount_to_withdraw = round(
                        amount_to_receive * exchange.euro_to_usd, 2
                    )
                    return (
                        balance[2] >= amount_to_withdraw
                        and balance[1] >= amount_to_receive
                    )
            else:
                return False  # Обработка несуществующей валюты

    """Обмен валют"""

    def exchange_currency(
        self,
        amount_to_receive: float,
        from_currency: str,
        to_currency: str,
        user_id: int,
        exchange: ExchangeRate,
    ) -> None:
        if amount_to_receive <= 0:
            print("Нельзя обменивать нулевую или отрицательную сумму.")
            return

        with sqlite3.connect(self.db_name) as db:
            cur = db.cursor()

            try:
                if from_currency == "RUB":
                    if to_currency == "USD":
                        amount_to_withdraw = round(
                            amount_to_receive * exchange.usd_to_rub, 2
                        )
                        cur.execute(
                            f"""UPDATE {self.table_name}
                                    SET Balance_RUB = Balance_RUB - ?,
                                    Balance_USD = Balance_USD + ?
                                    WHERE UserID = ?
                                """,
                            (amount_to_withdraw, amount_to_receive, user_id),
                        )
                    elif to_currency == "EUR":
                        amount_to_withdraw = round(
                            amount_to_receive * exchange.euro_to_rub, 2
                        )
                        cur.execute(
                            f"""UPDATE {self.table_name}
                                    SET Balance_RUB = Balance_RUB - ?,
                                    Balance_EUR = Balance_EUR + ?
                                    WHERE UserID = ?
                                """,
                            (amount_to_withdraw, amount_to_receive, user_id),
                        )
                elif from_currency == "USD":
                    if to_currency == "RUB":
                        amount_to_withdraw = round(
                            amount_to_receive / exchange.usd_to_rub, 2
                        )
                        cur.execute(
                            f"""UPDATE {self.table_name}
                                    SET Balance_USD = Balance_USD - ?,
                                    Balance_RUB = Balance_RUB + ?
                                    WHERE UserID = ?
                                """,
                            (amount_to_withdraw, amount_to_receive, user_id),
                        )
                    elif to_currency == "EUR":
                        amount_to_withdraw = round(
                            amount_to_receive * exchange.usd_to_euro, 2
                        )
                        cur.execute(
                            f"""UPDATE {self.table_name}
                                    SET Balance_USD = Balance_USD - ?,
                                    Balance_EUR = Balance_EUR + ?
                                    WHERE UserID = ?
                                """,
                            (amount_to_withdraw, amount_to_receive, user_id),
                        )
                elif from_currency == "EUR":
                    if to_currency == "RUB":
                        amount_to_withdraw = round(
                            amount_to_receive / exchange.euro_to_rub, 2
                        )
                        cur.execute(
                            f"""UPDATE {self.table_name}
                                    SET Balance_EUR = Balance_EUR - ?,
                                    Balance_RUB = Balance_RUB + ?
                                    WHERE UserID = ?
                                """,
                            (amount_to_withdraw, amount_to_receive, user_id),
                        )
                    elif to_currency == "USD":
                        amount_to_withdraw = round(
                            amount_to_receive * exchange.euro_to_usd, 2
                        )
                        cur.execute(
                            f"""UPDATE {self.table_name}
                                    SET Balance_EUR = Balance_EUR - ?,
                                    Balance_USD = Balance_USD + ?
                                    WHERE UserID = ?
                                """,
                            (amount_to_withdraw, amount_to_receive, user_id),
                        )
                else:
                    print("Неверная валюта")
                    return

                print("Обмен валюты успешно завершен")
            except Exception as e:
                db.rollback()  # Отменить изменения при ошибке
                print(f"Ошибка при обмене валюты: {e}")
