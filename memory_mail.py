#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
import sys
import time
import memory_general
from email.mime.text import MIMEText
from email.header import Header

reload(sys)
sys.setdefaultencoding('utf-8')

def send_email(mail_subject, mail_text):
    sender = ("%s<??????@aws.com>") % (Header('sender header','utf-8'),)
    receivers = ['??????@icloud.com']
    
    msg = memory_general.mail_format(mail_text)
    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header("message_from_text", 'utf-8')
    message['To'] =  Header("message_to_text", 'utf-8')
    
    mail_subject = time.strftime("%m-%d", time.localtime()) + ' ' + \
        mail_subject
    message['Subject'] = Header(mail_subject, 'utf-8').encode()
    
    
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "send email successful"
    except smtplib.SMTPException:
        print "Error: can not send email"
