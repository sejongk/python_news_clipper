import os
import time
import base64

import smtplib
from email.mime.text import MIMEText


def create_mail_content(content):
    with open('mail_base.html', 'r') as f:
        base_html = f.read()
    return base_html.format(content)


def send_mail(content):
    print(os.environ['MAIL_SENDER_EMAIL'])
    sender_email = base64.b64decode(os.environ['MAIL_SENDER_EMAIL']).decode('utf-8')
    sender_password = base64.b64decode(os.environ['MAIL_SENDER_PASSWORD']).decode('utf-8')
    receiver_emails = os.environ['MAIL_RECEIVER_EMAILS'].split(":")

    smtpName = 'smtp.naver.com' #smtp 서버 주소
    smtpPort = 587 #smtp 포트 번호
    
    for receiver_email in receiver_emails: 
        s=smtplib.SMTP( smtpName , smtpPort ) 
        s.starttls() 
        s.login(sender_email , sender_password) 

        msg = MIMEText(content , _subtype='html', _charset = "utf8") # MIMEText(text)
        msg['Subject'] ='{} News Clippings'.format(time.strftime('%Y-%m-%d, %H시', time.localtime(time.time())))
        msg['From'] = sender_email
        msg['To'] = receiver_email
        s.sendmail(sender_email, receiver_email, msg.as_string())
        
        s.close()