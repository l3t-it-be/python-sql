from dataclasses import dataclass
from selene import browser, query
from selene.support.shared.jquery_style import s, ss
from selenium import webdriver


@dataclass
class ExchangeRate:
    usd_to_rub: float
    euro_to_rub: float
    usd_to_euro: float
    euro_to_usd: float


class Currencies:
    """Получение курсов валют"""

    def __init__(self):
        """Настраиваем работу браузера"""
        browser_options = webdriver.ChromeOptions()
        browser_options.page_load_strategy = 'eager'
        browser_options.add_argument('--headless')
        browser.config.driver_options = browser_options

    @staticmethod
    def get_exchange_rate(search: str) -> float:
        """Получаем курс валют"""
        browser.open('https://www.google.com/')
        s('[name="q"]').clear().type(search).press_enter()
        value = ss('[data-attrid="Converter"] input')[1].get(
            query.attribute('value')
        )
        return float(value)


def get_exchange_rates():
    currency = Currencies()
    try:
        rates = list(
            map(
                currency.get_exchange_rate,
                ['usd to rub', 'euro to rub', 'usd to euro', 'euro to usd'],
            )
        )
        return ExchangeRate(*rates)
    except Exception as error:
        print(error)
        return None


exchange_rates = get_exchange_rates()
