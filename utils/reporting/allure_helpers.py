from pathlib import Path

import rootpath
from playwright.sync_api import Browser, Page

from core.environment_variables_setup import ENVIRONMENT_NAME


def setup_allure_environment_file(browser: Browser, page: Page):
    """Generate Allure environment.properties file"""
    root = rootpath.detect()
    try:
        allure_environment = Path(f"{root}/allure-results/environment.properties")
        allure_environment.touch()
        allure_environment.write_text(
            f"Environment={ENVIRONMENT_NAME}\n"
            f"Browser_version={browser.version}\n"
            f"Window_size={page.viewport_size}"
        )
    except FileNotFoundError as e:
        raise FileNotFoundError("Allure Environment file cannot be generated!") from e
