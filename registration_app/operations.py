from config import config
from registration_app.enums import OperationChoice
from registration_app.sql_queries import UserManager


class Operation:
    @staticmethod
    def choose_operation() -> None:
        while True:
            print(config.CHOOSE_ACTION)
            print(config.REGISTRATION_1)
            print(config.AUTHORIZATION_2)
            print(config.RESET_PASSWORD_3)
            print(config.EXIT_4)

            choice = input(config.INPUT_NUMBER_OF_ACTION)

            with UserManager() as user:
                if choice == OperationChoice.REGISTER_NEW_USER:
                    user.register_new_user()
                elif choice == OperationChoice.AUTHORIZE_USER:
                    user.authorize_user()
                elif choice == OperationChoice.RESET_PASSWORD:
                    user.reset_password()
                elif choice == OperationChoice.EXIT:
                    print(config.MSG_EXIT)
                    break
                else:
                    print(config.INCORRECT_NUMBER)
