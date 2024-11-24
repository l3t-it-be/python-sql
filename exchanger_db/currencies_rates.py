from dataclasses import dataclass

from selene import browser, query
from selene.support.shared.jquery_style import s, ss
from selenium import webdriver


@dataclass(kw_only=True)
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


currency = Currencies()

usd_to_rub = currency.get_exchange_rate('usd to rub')
euro_to_rub = currency.get_exchange_rate('euro to rub')
usd_to_euro = currency.get_exchange_rate('usd to euro')
euro_to_usd = currency.get_exchange_rate('euro to usd')

exchange_rate = ExchangeRate(
    usd_to_rub=usd_to_rub,
    euro_to_rub=euro_to_rub,
    usd_to_euro=usd_to_euro,
    euro_to_usd=euro_to_usd,
)
