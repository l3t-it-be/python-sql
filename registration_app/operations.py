from config import ConfigStrings
from registration_app.enums import OperationChoice
from registration_app.sql_queries import UserManager

config = ConfigStrings()


class Operation:
    @staticmethod
    def choose_operation() -> None:
        while True:
            print(config.CHOOSE_ACTION)
            print(config.REGISTRATION)
            print(config.AUTHORIZATION)
            print(config.RESET_PASSWORD)
            print(config.EXIT)

            choice = input(config.INPUT_NUMBER)

            with UserManager('users_data') as user:
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
