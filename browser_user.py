# needed for patreon
import undetected_chromedriver as uc
from selenium import webdriver
from time import sleep


class BrowserUser:
    def __init__(self) -> None:
        # for grabbing multuple mods durring one session
        # removed
        # self.to_grab: list[str] = []
        # self.pages: dict[str, str] = []

        self.driver = BrowserUser.init_driver()

    @staticmethod
    def init_driver():
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument("--no-sandbox")
        return uc.Chrome(options=options)

    def grab_page_source(self, url: str, wait_time: float = 1):
        if self.driver == None:
            self.driver = BrowserUser.init_driver()

        self.driver.get(url)
        sleep(wait_time)
        return self.driver.page_source

    def start():
        sleep(7)
        pass

    def close_driver(self):
        self.driver.close()
