# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os
import time


class Mail:
    def __init__(self,adress,senders,reciver,title,text):
        # 第三方 SMTP 服务

        self.mail_host = "smtp.qq.com"  # 设置服务器:这个是qq邮箱服务器，直接复制就可以
        self.mail_pass = "sagbllorvslzdjjd"  # 刚才我们获取的授权码
        self.sender = '2221078665@qq.com' # 你的邮箱地址
        self.receivers = adress  # 收件人的邮箱地址，可设置为你的QQ邮箱或者其他邮箱，可多个
        self.senders = senders
        self.receiver = reciver
        self.text = text
        self.title = title

    def send(self):

        content = self.text   #内容
        message = MIMEText(content, 'plain', 'utf-8')

        message['From'] = Header(self.senders, 'utf-8')
        message['To'] = Header(self.receiver, 'utf-8')

        subject = self.title  # 发送的主题，可自由填写（标题）
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpObj.login(self.sender, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
            print('邮件发送成功')
        except smtplib.SMTPException as e:
            print('邮件发送失败')

        # 完成后关机/睡眠
        time.sleep(10)
        os.system('shutdown /h /f /t 60')

