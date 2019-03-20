from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from core.google import Google
from retry import retry
from conf.config import BROWSER
from conf.config import CURRENT_DATE
import os,re

class Browser:
    browserClient = None

    def _get_browser(self):
        if not Browser.browserClient:
            Browser.browserClient = Google().get_google()
        return Browser.browserClient

    def get_element(self, xpath):
        element = WebDriverWait(self._get_browser(), 20).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element

    def set_element_value(self, element, value, enter=False):
        '''
        给浏览器的某个元素设置值
        :param element: 元素
        :param value: 值
        :param enter: 是否回车
        :return:
        '''
        if isinstance(element, WebElement):
            element.send_keys(value)
        if enter:
            element.send_keys(Keys.ENTER)

    @retry(tries=3, delay=5, max_delay=10)
    def click_element(self, xpath,is_selector=False):
        '''
        单击某个元素
        :param xpath:
        :param is_selector: xpath是否为选中器
        '''
        if is_selector:
            WebDriverWait(self._get_browser(),30,5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,xpath))
            )
            self._get_browser().execute_script(xpath)
        else:
            WebDriverWait(self._get_browser(), 30,5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            self.get_element(xpath).click()

    def is_disabled(self, xpath):
        '''
        判断页面元素是否可以点击
        :param xpath:
        :return: True , 不可用， False  可用
        '''
        WebDriverWait(self._get_browser(), 30,5).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        if self._get_browser().find_element_by_xpath(xpath).get_attribute('disabled'):
            return True
        return False

    def is_selected(self, xpath):
        WebDriverWait(self._get_browser(), 20,5).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return self._get_browser().find_element_by_xpath(xpath).is_selected()

    def swith_iFrame(self, xpath):
        '''
        切换iFrame，支持两种方式，reference【即下标】 模式和  xpath模式
        :param xpath: 如果int为数字则切换为默认窗口中
        '''
        if isinstance(xpath, int):
            self._get_browser().switch_to.default_content()
        else:
            WebDriverWait(self._get_browser(), 20,5).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, xpath))
            )

    def swith_window(self, index):
        windows = self._get_browser().window_handles
        self._get_browser().switch_to.window(windows[index])

    def get_element_text(self, xpath):
        element = self.get_element(xpath)
        if isinstance(element, WebElement):
            return element.text
        return ''

    def get_element_attr(self, xpath, attr_name):
        element = self.get_element(xpath=xpath)
        if isinstance(element, WebElement):
            return element.get_attribute(attr_name)
        return ''

    def goto_target_url(self, url):
        self._get_browser().get(url)

    def judge_excel_type(self, directory, fileType):
        flag = True
        if isinstance(directory, list):
            for d in directory:
                if os.path.splitext(d)[1] == '.' + fileType:
                    flag = flag & True
                else:
                    flag = False
        else:
            flag = False
        return flag

    def quit(self):
        self._get_browser().quit()
        #单例模式下必须清零
        Browser.browserClient = None

    def refresh(self):
        self._get_browser().refresh()

    @classmethod
    def browser_download_files(self, pattern, dir_path=None):

        if not dir_path:
            dir_path = os.path.join(BROWSER.get('google').get('download'),CURRENT_DATE)
        files = []
        for f in os.listdir(dir_path):
            if pattern is not None:
                result = re.search(r'' + pattern, os.path.splitext(f)[0])
                if result:
                    files.append(os.path.basename(f))
            else:
                files.append(os.path.basename(f))
        return files

    def getShutpng(self, image_name):
        result = self._get_browser().get_screenshot_as_file(
            os.path.join(BROWSER.get('google').get('download'), image_name)
        )

    def scroll_top(self):
        self._get_browser().execute_script(
            'document.documentElement.scrollTop=10000'
        )

    def get_browser_size(self):
        return self._get_browser().get_window_size()
