import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email:
    def __init__(self):
        self.mail_host = 'smtp.exmail.qq.com'
        self.mail_user = 'xxxxxxxxxx'
        self.mail_passwd = 'xxxxxxxxxxxxxxx'
        self.mail_port = '465'
        self.receivers = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    def send(self,content):
        try:
            smtp = smtplib.SMTP_SSL(self.mail_host, self.mail_port)
            smtp.login(self.mail_user, self.mail_passwd)
            smtp.sendmail(self.mail_user, self.receivers, self._getMessage(content).as_string())
            smtp.quit()
            print('success')
        except smtplib.SMTPException as e:
            print(e)


    def _getMessage(self,content):
        msg = MIMEMultipart('mixed')
        msg['Subject'] = 'Mabang  Scrapy Error ！！！'
        msg['From'] = self.mail_user
        msg['To'] = self.receivers
        msg_html = MIMEText(content, 'html', 'utf-8')
        # 添加html节点到 mimemultipart 对象中去
        msg.attach(msg_html)
        return msg