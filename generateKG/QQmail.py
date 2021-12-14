# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart


class Mail:
    def __init__(self,adress,senders,reciver,title,text,filename):
        # 第三方 SMTP 服务

        self.mail_host = "smtp.qq.com"  # 设置服务器:这个是qq邮箱服务器，直接复制就可以
        self.mail_pass = "sagbllorvslzdjjd"  # 刚才我们获取的授权码
        self.sender = '2221078665@qq.com' # 你的邮箱地址
        self.receivers = adress  # 收件人的邮箱地址，可设置为你的QQ邮箱或者其他邮箱，可多个
        self.senders = senders
        self.receiver = reciver
        self.text = text
        self.title = title
        self.filename = filename

    def send(self):
        message = MIMEMultipart()
        # MIMEText(content, 'plain', 'utf-8')

        message['From'] = Header(self.senders, 'utf-8')
        message['To'] = Header(self.receiver, 'utf-8')
        message['Subject'] = Header(self.title, 'utf-8')   # 发送的主题，可自由填写（标题）
        message.attach(MIMEText(self.text, 'plain', 'utf-8'))  #text:内容
        att = MIMEText(open(self.filename).read(),'base64','utf8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = f"attachment; filename={self.filename}"
        message.attach(att)
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpObj.login(self.sender, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
            print('邮件发送成功')
        except smtplib.SMTPException as e:
            print('邮件发送失败')











