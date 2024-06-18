from dataclasses import dataclass

import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from core.environment_variables_setup import LONG_TIMEOUT
from utils.playwright import PlaywrightSyncEngine
from utils.reporting.allure_helpers import setup_allure_environment_file


@dataclass
class PwDriver:
    page: Page
    browser: Browser


def get_driver() -> tuple[Page, Browser]:
    # Run local browser in incognito mode
    pw_engine = PlaywrightSyncEngine().engine
    browser = pw_engine.chromium.launch(channel="chrome", headless=False)
    view_port = {"width": 1440, "height": 900}

    context: BrowserContext = browser.new_context(
        viewport=view_port,
        permissions=["notifications", "clipboard-read", "clipboard-write"],
    )
    page = context.new_page()

    page.set_default_timeout(LONG_TIMEOUT)
    page.set_default_navigation_timeout(LONG_TIMEOUT)

    setup_allure_environment_file(browser, page)

    return page, browser


@pytest.fixture
def driver() -> PwDriver:
    page, browser = get_driver()

    yield PwDriver(page=page, browser=browser)

    browser.close()
