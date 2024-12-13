import csv
import os

from config import config


class Report:
    @staticmethod
    def create_csv() -> None:
        """Создание файла для отчетов"""
        with open(config.FILE_FOR_MOBILE_REPORTS, 'a', newline='') as csvfile:
            data = config.DATA_FOR_MOBILE_REPORTS
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerows(data)
        print(config.FILE_FOR_MOBILE_REPORTS_CREATED)

    def report_operation(
        self, date: str, operator: str, count_min: int, amount: int
    ) -> None:
        """Запись данных о звонке в CSV-файл"""
        # Проверка существования файла и его создание, если он не существует
        if not os.path.exists(config.FILE_FOR_MOBILE_REPORTS):
            self.create_csv()

        with open(config.FILE_FOR_MOBILE_REPORTS, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow([date, operator, count_min, amount])
        print(
            config.SUCCESSFUL_CALL,
            date,
            operator,
            count_min,
            config.MINUTES,
            amount,
            config.RUB_RUS,
        )
        print(config.DATA_REPORTED, config.FILE_FOR_MOBILE_REPORTS)


report = Report()
