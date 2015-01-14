#!/usr/bin/env python
import os, sys
import smtplib
import string
from configobj import ConfigObj

def send_email(subject, to_addr, body_text):
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "config.ini")
 
    if os.path.exists(config_path):
        cfg = ConfigObj(config_path)
        cfg_dict = cfg.dict()
    else:
        print "Config not found! Exiting!"
        sys.exit(1)
 
    host = cfg_dict["server"]
    from_addr = cfg_dict["from_addr"]
    password = cfg_dict["password"]
 
    BODY = string.join((
            "From: %s" % from_addr,
            "To: %s" % to_addr,
            "Subject: %s" % subject ,
            "",
            body_text
            ), "\r\n")
    server = smtplib.SMTP(host)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], BODY)
    server.quit()
 
if __name__ == "__main__":
    subject = "Test email from Python"
    to_addr = "wangfei@cyou-inc.com"
    body_text = "Greetings from Python"
    send_email(subject, to_addr, body_text)

'''
config file should place along with the python script
and looks as follow:

server = smtp.163.com
from_addr = xxxx@163.com
password = xxxxxxxx

'''
