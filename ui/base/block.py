from abc import ABCMeta
from typing import List

from playwright.sync_api import TimeoutError as TimeoutErr

from core.environment_variables_setup import DEFAULT_TIMEOUT, NO_TIMEOUT
from ui.base.html_element import HtmlElement
from utils.reporting.ui_coverage_helpers import record_locator


# pylint: disable=too-many-arguments


class BaseBlock(HtmlElement, metaclass=ABCMeta):
    """The base abstract class from which every block of HTML elements must inherit.
    Also, simple elements that contain HtmlElements (e.g. BaseFilter,
    MarketSelector, etc.) must inherit this class.
    """

    def _find_html_element(
        self,
        xpath: str,
        timeout: int = DEFAULT_TIMEOUT,
        element_class: HtmlElement = HtmlElement,
        highlight: bool = True,
        visible: bool = True,
        outer_search: bool = False,
    ) -> HtmlElement:
        """Find element or a block by XPATH and cast it to specified class

        :param xpath:
            Locator value (e.g. '"//div[contains(@class, 'graph-and-table-container')]"')
        :param timeout:
            Time to wait until element is displayed
        :param element_class:
            Custom HtmlElement class (e.g. TextField, Checkbox etc.) to convert the found element to
        :param highlight:
            Set this to False if you need to avoid highlighting for this element
        :param visible:
            Defines if the element is expected to be visible
            Set it to False if you need to find 'input' element which is not visible
        :param outer_search:
            Defines if the search should be performed from the page root.

        :return: the found HtmlElement (or simple element) object
        """
        root = self.page if outer_search else self.element
        pw_locator = root.locator(f"xpath={xpath}").first

        record_locator(
            self.page.url,
            pw_locator,
            is_block=issubclass(element_class, BaseBlock),
            outer_search=outer_search,
            outer_xpath=xpath,
        )
        if visible:
            pw_locator.wait_for(timeout=timeout)

        # noinspection PyCallingNonCallable
        element = element_class(pw_locator)

        if highlight:
            element.highlight()

        return element

    def _find_html_elements(
        self,
        xpath: str,
        timeout: int = DEFAULT_TIMEOUT,
        element_class: HtmlElement = HtmlElement,
        highlight: bool = True,
        visible: bool = True,
        outer_search: bool = False,
        force_wait: bool = False,
    ) -> List[HtmlElement]:
        """Find elements or blocks by XPATH and cast them to specified class

        Parameters
        ----------
        :param xpath:
            Locator value (e.g. '"//div[contains(@class, 'graph')]"')
        :param timeout:
            Timeout in milliseconds to wait until elements are displayed
        :param element_class:
            Custom HtmlElement class (e.g. TextField, Checkbox etc.)
            to cast the found elements to
        :param highlight:
            Set this to False if you need to avoid highlighting for this element.
            Sometimes highlighting can break the page structure.
        :param visible:
            Defines if elements are expected to be visible.
        :param outer_search:
            Defines if the search should be performed from the page root.
        :param force_wait:
            Set this to True if you need to wait for at least one element to displayed.
            Set (force_wait=True, visible=False) if you wait until an element is attached.

            Default value is False. It means that if no elements are found,
            the method will return an empty list.
        """
        root = self.page if outer_search else self.element
        pw_locator = root.locator(f"xpath={xpath}")

        if force_wait:
            state = "visible" if visible else "attached"
            pw_locator.first.wait_for(timeout=timeout, state=state)

        pw_elements = [pw_locator.nth(x) for x in range(pw_locator.count())]

        _ = [
            record_locator(
                self.page.url,
                pw_elem,
                is_block=issubclass(element_class, BaseBlock),
                outer_search=outer_search,
                outer_xpath=xpath,
            )
            for pw_elem in pw_elements
        ]
        if pw_elements and visible:
            pw_locator.first.wait_for(timeout=timeout)

        # noinspection PyCallingNonCallable
        elements = [element_class(el) for el in pw_elements]

        if highlight:
            _ = [x.highlight() for x in elements]

        return elements

    def _wait_element_to_appear(
        self,
        xpath: str,
        timeout: int = DEFAULT_TIMEOUT,
        message: str = None,
        outer_search: bool = False,
    ) -> bool:
        element = self._find_html_element(
            xpath, timeout=NO_TIMEOUT, visible=False, outer_search=outer_search
        )
        element.to_be_visible(timeout=timeout, message=message)

    def _wait_element_to_disappear(
        self,
        xpath: str,
        timeout: int = DEFAULT_TIMEOUT,
        message: str = None,
        outer_search: bool = False,
    ) -> bool:
        element = self._find_html_element(
            xpath, timeout=NO_TIMEOUT, visible=False, outer_search=outer_search
        )
        element.not_to_be_visible(timeout=timeout, message=message)

    def _is_html_element_displayed(
        self, xpath: str, timeout: int = None, outer_search: bool = False
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
                    xpath, timeout=NO_TIMEOUT, visible=False, outer_search=outer_search
                ).to_be_visible(timeout=timeout)
                return True
            except (TimeoutErr, AssertionError):
                return False

        return self._find_html_element(
            xpath, timeout=NO_TIMEOUT, visible=False, outer_search=outer_search
        ).is_displayed()
