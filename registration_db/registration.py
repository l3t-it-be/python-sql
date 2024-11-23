from operations import Operation
from sql_queries import UserManager


class Registration:
    @staticmethod
    def registration_logic():
        user = UserManager()
        user.create_table()
        user.add_new_user("Ivan", "qwer1234", "1234")
        operation = Operation()
        operation.choose_operation()


start = Registration
start.registration_logic()
