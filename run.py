from core.browser import Browser
from controller.login import Login
from controller.product import Product
from controller.excel import Excel
from controller.email import Email
from controller.dingding import Dingding
from retry import retry
from conf.config import *
import logging, os, traceback, sys,time

logging.basicConfig(
    filename=os.getcwd() + '/log/error.log',
    level=logging.ERROR,
    format="time:%(asctime)s \t levelname:%(levelname)s \n msg:%(message)s"
)
@retry(tries=3,delay=5,max_delay=20)
def scrapy_product():
        try:
            Login().login()
            Product.correct_sku_timer()
            Product().operate()
        except Exception:
            msg = traceback.format_exception(*sys.exc_info())
            logging.error(
                ''.join(msg)
            )
            raise Exception(''.join(msg))
        finally:
            Browser().quit()
            print('do again!!!!')


if __name__ == '__main__':
    params = sys.argv
    if len(params) > 1:
        start_time = time.time()
        content = Excel(title=Product.title).read_excel(filename=params[1], date=params[2], start=int(params[3]), length=int(params[4]))
        print(content)
        print(time.time()-start_time)
        exit(1)
    else:
        try:
            #10 mim to run 
            scrapy_product()
            if Product.get_page_timer() == IS_END:
            #     # 合并文件
                Excel(Product.file_rule, Product.title_ch, Product.title).combination_files('product_'+CURRENT_DATE+'.xlsx')
                Product().send_dingding()

                #发送钉钉信息
        except Exception as e:
            Email().send("".join(str(e)))