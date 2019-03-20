from core.browser import Browser
from controller.dingding import Dingding
from conf.config import *
from retry import retry
import re, time


class Product(Browser,Dingding):
    file_rule = '^\d{10}$'
    target_file_rule = '^product.*'
    title_ch = PRODUCT_TITLE_CH
    title = list(PRODUCT_TITLE.keys())
    title_index = list(PRODUCT_TITLE.values())
    single_filename = 'product.txt'

    def __init__(self):
        self.url = PATH_INFO.get('product')
        self.next_flag = 'getPaginationData'
        current_page = self.get_page_timer()
        if current_page != IS_END:
            self.current_page = int(current_page) + 1
        else:
            self.current_page = 1
        self.total_page = 0
        self.robot_content_prefix =  ''.join([ROBOT.get('ROBOT_COMMON_URL'), '?t=', CURRENT_DATE,'&c=product', '&f='])
        self.robot_url = ROBOT.get('PRODUCT').get('ROBOT_URL')

    @classmethod
    def set_page_timer(self, page=None):
        if not page:
            page = '1'
        with open(os.path.join(os.getcwd(), 'single', Product.single_filename), 'w') as f:
            f.write(str(page))

    @classmethod
    def get_page_timer(self):
        with open(os.path.join(os.getcwd(), 'single', Product.single_filename), 'r') as f:
            content = f.readline()
        return content

    def get_title_ch(self):
        return Product.title_ch

    def get_title(self):
        return Product.title

    def operate(self):
        self.set_page_timer(self.current_page)
        self.index()
        self.click_sku_column()
        self.goto_iFrame()
        self.set_export_page()
        self.swith_window(-1)
        self.init_sku_page()
        self.download_excle()

    @retry(tries=3, delay=5)
    def index(self):
        try:
            self.click_element('//*[@id="first-contents"]/li[3]')
        except Exception:
            self.refresh()
            raise Exception('is not clickable at point')

    def click_sku_column(self):
        self.click_element('//*[@id="M0010400"]/li[3]')

    def goto_iFrame(self):
        self.swith_iFrame('//*[@id="iframeContent"]')

    def set_export_page(self):
        self.click_element('//*[@id="main"]/div[1]/div[1]/div[1]/div/ul[2]/li[1]/div[1]/ul/li[1]')
        self.click_element('//*[@id="main"]/div[1]/div[1]/div[2]/div[1]/div[8]/button')
        self.click_element('//*[@id="main"]/div[1]/div[1]/div[2]/div[1]/div[8]/ul/li[10]')

    def set_export_filed(self):
        for element in Product.title_index:
            self.click_element('//*[@id="allfield"]/div[2]/div[1]/div/label[{0}]'.format(element))

    def init_sku_page(self):
        self.set_element_value(
            self.get_element('//*[@id="searchpagediv"]/div[2]/input'),
            self.current_page
        )
        self.click_element('//*[@id="searchpagediv"]/div[2]/button')

    def download_excle(self):
        total_pages = self.get_pages_num()
        self.set_export_filed()
        print('总页数:', total_pages)
        if not total_pages[1]:
            raise Exception('not page download')
        else:
            self.total_page = total_pages[1]

        while True:
            if not self.not_finish_download() and self.current_page > int(total_pages[1]):
                self.set_page_timer(IS_END)
                break

            print('当前页:', self.current_page)
            self.click_element('//*[@id="exportsaveas"]/button')
            time.sleep(10)
            # 此处有问题，点击焦点被抢走了,此处设置截屏
            self.click_element('//*[@id="searchpagediv"]/div[1]/button[7]')
            self.set_page_timer(self.current_page)
            self.current_page = self.current_page + 1

    def not_finish_download(self):
        '''
        判断是否还有下一页
        :return: 有，则返回一个list eg: [2,3000] ; 没有，返回False
        '''
        attr = self.get_element_attr('//*[@id="searchpagediv"]/div[1]/button[7]', 'onclick')
        if self.next_flag in attr:
            return re.findall(r'\d+', attr)
        return False

    def is_end(self):
        '''
        是否结束
        :return:
        '''
        if int(self.get_pages_num()[1]) >= self.current_page:
            return True

    def get_pages_num(self):
        '''
        :return: 返回list ,eg : ['59205', '20', '3000']
        '''
        info = self.get_element_text('//*[@id="searchpagediv"]/p')
        print('info :', type(info), '***', info)
        page_info = re.findall(r'\d+', info)
        if len(page_info) >= 2:
            return page_info
        raise Exception('can not get pages!!')

    @classmethod
    def correct_sku_timer(self):
        correct_file_num = len(Browser.browser_download_files(Product.file_rule))
        if correct_file_num > FILE_MIN_NUM:
            Product.set_page_timer(correct_file_num)

    def send_dingding(self):
        Dingding().send_max_dingding(
            Browser.browser_download_files(Product.target_file_rule),
            self.robot_url,
            self.robot_content_prefix
        )