import pathlib
import re
from typing import List, Union

from playwright.sync_api import FilePayload, Locator, expect
from playwright.sync_api import TimeoutError as TimeoutErr

from core.environment_variables_setup import (
    MIN_TIMEOUT,
    NO_TIMEOUT,
    LONG_TIMEOUT,
    DEFAULT_TIMEOUT,
)
from core.reporting.allure_helpers import attach_text_to_allure


class HtmlElementWrappedProperties:
    def __init__(self, locator: Locator):
        self.element = locator

    @property
    def page(self):
        return self.element.page

    @property
    def value(self):
        return self.element.get_attribute("value")

    @property
    def text(self) -> str:
        return self.element.inner_text()

    @property
    def text_content(self):
        """Returns the text content of the element, including its descendants.
        Note: Use for React elements like: svg, text, g, etc.
        """
        return self.element.text_content()

    @property
    def bounding_box(self):
        return self.element.bounding_box()

    @property
    def location(self):
        return self.element.bounding_box()


class HtmlElementWrappedMethods:
    def __init__(self, locator: Locator):
        self.element = locator

    def highlight(self):
        """Adding red highlighting to found element on the web-page"""
        self.element.highlight()

    def click(self, timeout=LONG_TIMEOUT, no_wait_after=False, **kwargs):
        try:
            self.element.click(timeout=timeout, no_wait_after=no_wait_after, **kwargs)
        except TimeoutErr as e:
            attach_text_to_allure(str(e), "exception_text")
            xpath = e.message.split("waiting for locator")[1].split("\n")[0].strip()
            raise TimeoutErr(
                f"Error while clicking on element (timeout={timeout / 1000}s). "
                f"Xpath:\n{xpath}"
            ) from e

    def hover(self, timeout=LONG_TIMEOUT, no_wait_after=False, **kwargs):
        try:
            self.element.hover(timeout=timeout, no_wait_after=no_wait_after, **kwargs)
        except TimeoutErr as e:
            attach_text_to_allure(str(e), "exception_text")
            xpath = e.message.split("waiting for locator")[1].split("\n")[0].strip()
            raise TimeoutErr(
                f"Error while hovering over the element (timeout={timeout / 1000}s)."
                f" Xpath:\n{xpath}"
            ) from e

    def double_click(self, timeout=LONG_TIMEOUT, no_wait_after=False, **kwargs):
        try:
            self.element.dblclick(
                timeout=timeout, no_wait_after=no_wait_after, **kwargs
            )
        except Exception as e:
            attach_text_to_allure(str(e), "exception_text")
            raise Exception(
                f"Error while double clicking on the element (timeout={timeout / 1000})s"
            ) from e

    def double_click_force(self):
        self.double_click(force=True)

    def click_force(self, timeout=MIN_TIMEOUT):
        # has to be used with non-0 timeout, thus set a MIN_TIMEOUT by default
        self.click(force=True, timeout=timeout)

    def get_attribute(self, attribute_name: str):
        return self.element.get_attribute(attribute_name)

    def fill(self, value: str, force=False):
        self.element.fill(str(value), force=force)

    def upload_file(
        self,
        file_path: Union[
            str,
            pathlib.Path,
            FilePayload,
            List[Union[str, pathlib.Path]],
            List[FilePayload],
        ],
    ):
        self.element.set_input_files(file_path)

    def is_displayed(self):
        """Returns True if the element is visible, False otherwise.
        https://playwright.dev/python/docs/api/class-page#page-is-visible
        """
        return self.element.is_visible()

    def move_to(self):
        self.element.scroll_into_view_if_needed()

    def is_checked(self):
        return self.element.is_checked(timeout=DEFAULT_TIMEOUT)

    def select_option(self, value: str):
        self.element.select_option(value)

    def click_with_javascript(self):
        self.element.evaluate(
            """(element) => {
                if (element) {
                    element.click();
                }
            }""",
            self.element,
        )


class HtmlElementExpect:
    def __init__(self, locator: Locator):
        self.element = locator

    def to_have_css_attribute(
        self, name: str, value: Union[str, re.Pattern], timeout: int = NO_TIMEOUT
    ) -> bool:
        try:
            expect(self.element).to_have_css(name, value, timeout=timeout)
            return True
        except Exception:
            return False

    def to_be_checked(self, timeout=MIN_TIMEOUT) -> None:
        expect(self.element).to_be_checked(timeout=timeout)

    def not_to_be_checked(self, timeout=MIN_TIMEOUT) -> None:
        expect(self.element).not_to_be_checked(timeout=timeout)

    def not_to_be_visible(self, timeout=MIN_TIMEOUT, message: str = None) -> None:
        """Wait for the element to be hidden.
        Use only in combination with elements properties having "visible=False".

        Examples
        --------

        @property
        def modal_window(self) -> HtmlElement:
            return self._find_html_element("//div[@id='modal']", timeout=NO_TIMEOUT, visible=False)

        def close_modal_window(self):
            self.close_modal_button.click()
            self.modal_window.not_to_be_visible()

        Parameters
        ----------
        timeout:
            Maximum time to wait for in milliseconds. Defaults to 3000 (3 seconds).
        message:
            Optional custom error message to throw instead of the default error message.
        """
        try:
            expect(self.element).not_to_be_visible(timeout=timeout)
        except (TimeoutErr, AssertionError) as e:
            message = (
                message
                if message
                else f"Element is still visible after {timeout} ms: {self.element}"
            )
            raise AssertionError(message) from e

    def to_be_visible(self, timeout=MIN_TIMEOUT, message: str = None) -> None:
        try:
            expect(self.element).to_be_visible(timeout=timeout)
        except (TimeoutErr, AssertionError) as e:
            message = (
                message
                if message
                else f"Element is not visible after {timeout} ms: {self.element}"
            )
            raise AssertionError(message) from e

    def to_be_disabled(self, timeout=MIN_TIMEOUT, message: str = None) -> None:
        try:
            expect(self.element).to_be_disabled(timeout=timeout)
        except (TimeoutErr, AssertionError) as e:
            message = (
                message
                if message
                else f"Element is not disabled after {timeout} ms: {self.element}"
            )
            raise AssertionError(message) from e


class HtmlElement(
    HtmlElementWrappedMethods, HtmlElementWrappedProperties, HtmlElementExpect
):
    """Extending the Playwright web element object.
    Every simple web element (such as TextField) must inherit from this class.
    """

    def __get_center_coordinates_of_element(self):
        box = self.bounding_box
        assert box is not None
        x_center = box["x"] + box["width"] / 2
        y_center = box["y"] + box["height"] / 2
        return x_center, y_center

    def click_on_hovered(self, timeout=LONG_TIMEOUT):
        """clicks on hovered the element"""
        self.hover(timeout=timeout)
        self.click(timeout=timeout)

    def click_with_offset(self, x_offset, y_offset):
        """Moves from the element with offset and click the Left mouse button."""
        x_center, y_center = self.__get_center_coordinates_of_element()
        self.page.mouse.click(x_center + x_offset, y_center + y_offset, button="left")

    def double_click_force_with_offset(self, x_offset, y_offset):
        """Move the mouse by an offset of the specified element and
        double click with force on the space"""
        self.element.hover(position={"x": x_offset, "y": y_offset})
        self.double_click(force=True)

    def drag_and_drop_with_offset(self, x_offset: int = 0, y_offset: int = 0):
        """Holds down the left mouse button in the center of the source element,
        then moves to the target offset and releases the mouse button."""
        x_center, y_center = self.__get_center_coordinates_of_element()
        self.page.mouse.move(x_center, y_center)
        self.page.mouse.down()
        self.page.mouse.move(x_center + x_offset, y_center + y_offset, steps=10)
        self.page.mouse.up()

    def drag_and_drop_from_exact_point_with_offset(
        self, x_point: int = 0, y_point: int = 0, x_offset: int = 0, y_offset: int = 0
    ):
        """Holds down the left mouse button on the x/y coordinates from the source element's center,
        then moves to the target offset and releases the mouse button."""
        x_center, y_center = self.__get_center_coordinates_of_element()

        # move mouse to the exact point of the element counting from its center
        self.page.mouse.move(x_center + x_point, y_center - y_point)
        self.page.mouse.down()
        self.page.mouse.move(x_center + x_offset, y_center + y_offset, steps=10)
        self.page.mouse.up()

    def send_keys_with_js(self, text: str):
        """Type text into the element using Javascript"""
        try:
            self.element.evaluate(f"arguments[0].click();arguments[0].value='{text}';")
            self.element.evaluate("arguments[0].click();")
            self.element.evaluate("arguments[0].submit();")
        except Exception:
            self.element.fill(text)

    def hover_on(self):
        """hover the element"""
        self.element.hover()
