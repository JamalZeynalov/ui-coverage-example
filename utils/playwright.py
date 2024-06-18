from playwright.sync_api import sync_playwright
from singleton_decorator import singleton


@singleton
class PlaywrightSyncEngine:
    def __init__(self):
        self.engine = sync_playwright().start()
