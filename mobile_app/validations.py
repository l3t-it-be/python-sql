from config import config


class Validation:
    @staticmethod
    def get_valid_months_input() -> int:
        while True:
            try:
                months = int(input(config.INPUT_MONTHS_QUANTITY))
                return months
            except ValueError:
                print(config.INCORRECT_VALUE)
                while True:
                    choice = input(config.WISH_TO_CONTINUE).strip().lower()
                    if choice == config.YES:
                        break
                    elif choice == config.NO:
                        print(config.MSG_EXIT)
                        exit()
                    else:
                        print(config.INCORRECT_CHOICE)


validation = Validation()
