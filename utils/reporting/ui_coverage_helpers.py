import inspect
import re
from urllib.parse import urlparse

from playwright.sync_api import Locator

from conftest import used_locators


def get_test_allure_id_and_title() -> tuple[str, str]:
    """Find the test function and extract the allure_id and test title from annotations."""
    functions = inspect.getouterframes(inspect.currentframe())
    test_function = [x for x in functions if x.function.startswith("test_")][
        0
    ].frame.f_back.f_locals.get("testfunction")
    test_id_annotations = [
        x
        for x in test_function.pytestmark
        if x.name == "allure_label" and "as_id" in x.kwargs.values()
    ]
    test_id = test_id_annotations[0].args[0] if test_id_annotations else None

    # In case allure title is absent, use the function name
    test_title = (
        test_function.__allure_display_name__
        if hasattr(test_function, "__allure_display_name__")
        else test_function.__name__
    )

    return test_id, test_title


def _normalize_url(url: str):
    """Remove all query parameters and other not needed fragments from the URL.
    All IDs in the path will be replaced with X to avoid duplicates.
    The URL will be normalized to the base path.

    Parameters
    ----------
    url: str
        The original URL to be normalized.

    Examples
    --------
    Originals - https://example.com/path/to/page?param1=value1&param2=value2#tab1
                https://example.com/path/item/1/
    Normalized - https://example.com/path/to/page
                https://example.com/path/item/X

    """
    parsed_url = urlparse(url)

    # replace numbers with X to make URL abstract
    parsed_path = re.sub(r"\d+", "X", parsed_url.path)
    if parsed_path.endswith("/"):
        parsed_path = parsed_path[:-1]
    if url.endswith("/{}"):
        # remove string template parts. Occurs when test fails
        parsed_path = parsed_path.replace("/{}", "/X")
    if "#" in parsed_path:
        # remove added tabs names from url
        parsed_path = "".join(parsed_path.split("#")[:-1])

    return parsed_url.scheme + "://" + parsed_url.netloc + parsed_path


def _get_full_xpath(playwright_locator: "Locator"):
    """Extract the full xpath from the Playwright Locator object.
    Includes all parent elements up to the root.
    """
    raw_xpath: str = playwright_locator._impl_obj._selector

    # remove 'xpath=' from string
    locator: str = raw_xpath.replace("xpath=", "")

    # split string by ' >> nth=x >> ' pattern
    locator = locator.split(" >> ")

    return "".join(x for x in locator if "nth" not in x)


def record_locator(
    url: str,
    playwright_locator: "Locator",
    is_block: bool,
    outer_search: bool = False,
    outer_xpath: str = None,
):
    """
    Save used locator to the dictionary.
    The dictionary will be dumped to a JSON file after the test session is finished.
    File will be used by the UI Coverage tool to generate the report.

    Parameters
    ----------
    url: str
        The URL of the page where the element is located.
    playwright_locator: Locator
    is_block: bool
        Defines if the element is a block containing other elements.
    outer_search: bool
        Set True if the element is a block and the locator is not the direct parent.
        (e.g. being in the current block you want to find an element from another block)
    outer_xpath: str
        Set if you use outer_search=True. The outer_xpath xpath of the element you are looking for.
    """
    page_url = _normalize_url(url)
    parsed_xpath = _get_full_xpath(playwright_locator)
    allure_id, test_name = get_test_allure_id_and_title()

    outer_xpath = outer_xpath if outer_search else None

    # Add or update the data for the given page_url and full_xpath
    used_locators.setdefault(page_url, {}).setdefault(parsed_xpath, []).append(
        {
            "allure_id": allure_id,
            "is_block": is_block,
            "test_name": test_name,
            "original_page_url": url,
            "outer_xpath": outer_xpath,
        }
    )
