from abc import ABCMeta, abstractmethod

from playwright.sync_api import Browser, Page

from core.helpers.string_formatters import camelcase_name_to_words


# pylint: disable=unnecessary-dunder-call


class BaseApp(metaclass=ABCMeta):
    """The base abstract class from which every application should inherit"""

    def __init__(self, page: Page, browser: Browser = None):
        self.page = page
        self.browser = browser

    def __repr__(self):
        page_name = camelcase_name_to_words(self.__class__.__name__)
        return page_name

    def __str__(self):
        page_name = camelcase_name_to_words(self.__class__.__name__)
        return page_name

    @property
    @abstractmethod
    def base_url(self) -> str:
        raise NotImplementedError()

    def refresh_browser(self):
        self.page.reload()
