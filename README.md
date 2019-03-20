# 爬取采购数据

## 包含的功能
+		此爬虫实现了对马帮采购数据的爬取，
+		钉钉机器人自动推送的功能
+		邮件报警功能

### 使用说明：
1. 需要配置 `\conf\config.py` 和 `\controller\email.py` 这两个文件

### config.py 配置文件
```
from datetime import datetime
from collections import OrderedDict
import os
#browser config
BROWSER = {
    'google' : {
        'download' : os.path.join(os.getcwd(),'excels')
    }
}

ROBOT = {
    #自定义公用地址
    'ROBOT_COMMON_URL':'http://xxxxxxxxxxxxx:83',
    'PRODUCT':{
        #机器人地址
        'ROBOT_URL':'https://xxxxxxxxxxxxxxxxxxxxxx'
    }
}

FILE_MIN_NUM = 0

CURRENT_DATE = datetime.now().strftime('%Y%m%d')

#账户名和密码
USER_INFO = {
    'username' : 'xxxxx',
    'password' : 'xxxxxxxxxxxxxxxxxxxxxxxx'
}

PATH_INFO = {
    'login':'http://www.mabangerp.com',
    'product':'http://www.mabangerp.com/index.php?mod=stock.list&searchStatus=3'
}

IS_END = 'Ok'

PRODUCT_TITLE_CH = ['库存SKU', '库存SKU中文名称', '状态','是否带电' ,'商品父目录', '商品子目录', '库存总量', '未发货', '在途总量', '销量(7/28/42)', '重量', '图片链接','统一成本价', '采购价', '虚拟sku', '长', '宽', '高', '体积重', '创建时间', '供应商名称','采购链接','最新出库时间']

#value of label
PRODUCT_TITLE = OrderedDict([
    ('sku',1),('sku_ch',3),('status',6),('is_electricity',7),('parent_class',13),('sub_class',14),('sku_total',22),('no_deliver',23),('on_line',24),
    ('sales',25),('weight',26),('img_url',29),('unify_price',31),('cost_price',32),('virtual_sku',33),('length',36),('width',37),('height',38),
    ('volume',39),('create_time',40),('supplier_name',41),('purchase_url',46),('end_time',47)
])
```


### 邮件配置文件
```
//邮件服务器地址
self.mail_host = 'smtp.exmail.qq.com'
//邮件服务器登陆名
self.mail_user = 'xxxxxxxxxx'
//登陆密码
self.mail_passwd = 'xxxxxxxxxxxx'
self.mail_port = '465'
//邮件接收人地址
self.receivers = "xxxxxxxxxxxxxx"

```