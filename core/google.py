from conf import config
from selenium import webdriver
from datetime import datetime
import os


class Google:
    def __init__(self):
        self.download = os.path.join(
            config.BROWSER.get('google').get('download'),
            config.CURRENT_DATE
        )
        self.create_path(self.download)

    def _get_options(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('-start-maximized')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_experimental_option('prefs', {
            'profile.default_content_settings.popups': 0,
            'download.default_directory': self.download
        })
        return chrome_options

    def create_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def get_google(self):

        driver =  webdriver.Chrome(
            chrome_options=self._get_options()
        )
        driver.execute_script('window.resizeTo(1920, 1080)')
        return driver

