from playwright.sync_api import Playwright

from ui.base.app import BaseApp
from ui.pages.landing_page import LandingPage


class UltimateQa(BaseApp):
    def __init__(self, page, playwright: Playwright = None):
        super().__init__(page, playwright)
        self._main_page = LandingPage(page, self.base_url)

    @property
    def base_url(self) -> str:
        return "https://ultimateqa.com"

    @property
    def landing_page(self) -> LandingPage:
        return self._main_page
