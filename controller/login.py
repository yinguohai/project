from core.browser import Browser
from conf.config import *
class Login(Browser):
    def __init__(self):
        super(Login,self).__init__()
        self.username = USER_INFO.get('username')
        self.password = USER_INFO.get('password')
        self.url = PATH_INFO.get('login')

    def login(self):
        self.goto_target_url(self.url)
        self.set_element_value(
            self.get_element('//*[@id="username"]'),
            self.username
        )
        self.set_element_value(
            self.get_element('//*[@id="password"]'),
            self.password,
            True
        )