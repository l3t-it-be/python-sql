from attr import dataclass
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

    @staticmethod
    def get_exchange_rates() -> ExchangeRate:
        # Настраиваем работу браузера
        browser_options = webdriver.ChromeOptions()
        browser_options.page_load_strategy = 'eager'
        browser_options.add_argument('--headless')
        browser.config.driver_options = browser_options

        # Получаем курс доллара к рублю
        browser.open('https://www.google.com/')
        s('[name="q"]').type('usd to rub').press_enter()
        usd_to_rub = ss('[data-attrid="Converter"] input')[1].get(
            query.attribute('value')
        )

        # Получаем курс евро к рублю
        s('[name="q"]').clear().type('euro to rub').press_enter()
        euro_to_rub = ss('[data-attrid="Converter"] input')[1].get(
            query.attribute('value')
        )

        # Получаем курс доллара к евро
        s('[name="q"]').clear().type('usd to euro').press_enter()
        usd_to_euro = ss('[data-attrid="Converter"] input')[1].get(
            query.attribute('value')
        )

        # Получаем курс евро к доллару
        s('[name="q"]').clear().type('euro to usd').press_enter()
        euro_to_usd = ss('[data-attrid="Converter"] input')[1].get(
            query.attribute('value')
        )

        return ExchangeRate(
            usd_to_rub=float(usd_to_rub),
            euro_to_rub=float(euro_to_rub),
            usd_to_euro=float(usd_to_euro),
            euro_to_usd=float(euro_to_usd),
        )
