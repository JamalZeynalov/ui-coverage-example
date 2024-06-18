from abc import ABCMeta, abstractmethod
from typing import Callable, Pattern, Union

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as TimeoutErr

from core.environment_variables_setup import (
    DEFAULT_TIMEOUT,
    LONG_TIMEOUT,
    NO_TIMEOUT,
)
from core.helpers.string_formatters import camelcase_name_to_words
from ui.base.block import BaseBlock
from ui.base.html_element import HtmlElement
from utils.reporting.ui_coverage_helpers import record_locator


# pylint: disable=too-many-arguments


class BasePage(metaclass=ABCMeta):
    """The base abstract class from which every Page Object must inherit"""

    def __init__(self, page: Page, base_url: str):
        self._base_url = base_url
        self._driver = page

    def __repr__(self):
        page_name = camelcase_name_to_words(self.__class__.__name__)
        return page_name

    @property
    @abstractmethod
    def path(self) -> str:
        raise NotImplementedError()

    @property
    def url(self):
        return f"{self._base_url}{self.path}"

    @property
    def is_current_page(self):
        return self.url == self.get_current_url()

    def open_url(self, url: str):
        self._driver.goto(url, timeout=LONG_TIMEOUT * 2)

    def wait_for_url(
        self,
        url: Union[str, Pattern[str], Callable[[str], bool]],
        timeout: int = DEFAULT_TIMEOUT,
        message: str = None,
    ):
        """Wait until the current URL matches the exact string or specified pattern
        :param url:
            Exact URL or pattern to wait for
        :param timeout:
            Time in milliseconds to wait until expected URL is opened
        :param message:
            Custom message to be displayed in Allure report in case of failure
        """
        if message:
            msg = message
        elif not message and "*" in url:
            msg = (
                f"Current URL does not match the pattern '{url}' "
                f"after {int(timeout / 1000)} seconds"
            )
        else:
            msg = (
                f"Current URL is not '{url}' after {int(timeout / 1000)} seconds."
                f"\nActual URL is '{self.get_current_url()}'\n"
            )

        try:
            self._driver.wait_for_url(url, timeout=timeout)
        except TimeoutErr as err:
            raise AssertionError(msg) from err

    def open(self, timeout: int = DEFAULT_TIMEOUT):
        self._driver.goto(self.url, timeout=timeout)
        self.wait_for_url(self.url, timeout=timeout)

    def _find_html_element(
        self,
        xpath: str,
        timeout: int = DEFAULT_TIMEOUT,
        element_class=HtmlElement,
        highlight: bool = True,
        visible=True,
    ) -> HtmlElement:
        """Find element or block by XPATH and cast it to specified class
        :param xpath:
            Locator value (e.g. '"//div[contains(@class, 'graph-and-table-container')]"')
        :param timeout:
            Time to wait until element is displayed
        :param element_class:
            Custom HtmlElement class (e.g. TextField, etc.) to convert the found element to
        :param highlight:
            Set this to False if you need to avoid highlighting for this element
        :param visible:
            Defines if the element is expected to be visible
            Set it to False if you need to find 'input' element which is not visible

        :return: the found HtmlElement (or simple element) object
        """

        pw_locator = self._driver.locator(f"xpath={xpath}").first
        element = element_class(pw_locator)

        record_locator(
            self.url,
            pw_locator,
            is_block=issubclass(element_class, BaseBlock),
        )

        if visible:
            pw_locator.wait_for(timeout=timeout)
        if highlight:
            element.highlight()

        return element

    def _wait_element_to_appear(
        self,
        xpath: str,
        timeout: int = DEFAULT_TIMEOUT,
        message: str = None,
        wait_element_timeout: int = NO_TIMEOUT,
        visible: bool = False,
    ) -> None:
        self._find_html_element(
            xpath, timeout=wait_element_timeout, visible=visible
        ).to_be_visible(timeout=timeout, message=message)

    def _wait_element_to_disappear(
        self,
        xpath: str,
        timeout: int = DEFAULT_TIMEOUT,
        message: str = None,
        wait_element_timeout: int = NO_TIMEOUT,
        visible: bool = False,
    ) -> None:
        self._find_html_element(
            xpath, timeout=wait_element_timeout, visible=visible
        ).not_to_be_visible(timeout=timeout, message=message)

    def _is_html_element_displayed(
        self,
        xpath: str,
        timeout: int = None,
    ) -> bool:
        """Check if element is displayed

        :param xpath:
            Locator value (e.g. '"//div[contains(@class, 'graph-and-table-container')]"')
        :param timeout:
            Set timeout > 0.01 to wait for element to be displayed. Defaults to 0.
        """
        if timeout and timeout != NO_TIMEOUT:
            try:
                self._find_html_element(
                    xpath, timeout=NO_TIMEOUT, visible=False
                ).to_be_visible(timeout=timeout)
                return True
            except (TimeoutErr, AssertionError):
                return False

        return self._find_html_element(
            xpath, timeout=NO_TIMEOUT, visible=False
        ).is_displayed()

    def get_current_url(self):
        return self._driver.url
