from registration_app.operations import Operation
from registration_app.sql_queries import UserManager


class Registration:
    @staticmethod
    def registration_logic():
        with UserManager() as user:
            user.create_table()
            user.add_new_user('Ivan', 'qwer1234', '1234')
            operation = Operation()
            operation.choose_operation()


if __name__ == '__main__':
    start = Registration()
    start.registration_logic()
