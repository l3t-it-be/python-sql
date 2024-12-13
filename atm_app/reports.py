import csv
import os
from datetime import datetime

from config import config


class Report:
    @staticmethod
    def create_csv(filename: str) -> None:
        """Создание файла для отчетов"""
        with open(filename, 'a', newline='') as csvfile:
            if filename == config.FILE_FOR_REPORTS_1:
                data = config.DATA_FOR_REPORTS_1
            elif filename == config.FILE_FOR_REPORTS_2:
                data = config.DATA_FOR_REPORTS_2

            writer = csv.writer(csvfile, delimiter=';')
            writer.writerows(data)
        print(config.FILE_FOR_REPORTS_CREATED, filename)

    def report_operation(
        self,
        filename,
        card_number1: str,
        current_operation: str,
        amount: str,
        card_number2=None,
    ) -> None:
        """Запись данных в файл для отчета"""
        if amount is False:
            print(config.OPERATION_WAS_NOT_PERFORMED)
            return

        current_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        user_data = [current_date, card_number1, current_operation, amount]

        if filename == config.FILE_FOR_REPORTS_2:
            user_data.append(card_number2)

        # Проверка существования файла и его создание, если он не существует
        if not os.path.exists(filename):
            self.create_csv(filename)

        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(user_data)

        print(config.DATA_REPORTED, filename)
