import pytest

from ui.applications.ultimate_qa import UltimateQa


@pytest.fixture(params=[UltimateQa])
def ultimate_qa_app(driver):
    app = UltimateQa(driver.page, driver.browser)

    return app
