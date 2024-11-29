from config import config


class Validation:
    @staticmethod
    def get_valid_months_input() -> int:
        while True:
            months_input = input(config.INPUT_MONTHS_QUANTITY)
            if months_input.isdigit() and int(months_input) > 0:
                return int(months_input)
            else:
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
