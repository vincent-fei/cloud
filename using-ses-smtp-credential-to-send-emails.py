#!/usr/bin/env python
# -*- coding: utf-8 -*-
# wangfei [at] imbusy.me

import os, sys
import smtplib
import string
from configobj import ConfigObj

def send_email(subject, body_text, to_emails, cc_emails, bcc_emails):
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
    username = cfg_dict["username"]
    password = cfg_dict["password"]
 
    BODY = string.join((
            "From: %s" % from_addr,
            "To: %s" % ', '.join(to_emails),
            "CC: %s" % ', '.join(cc_emails),
            "BCC: %s" % ', '.join(bcc_emails),
            "Subject: %s" % subject ,
            "",
            body_text
            ), "\r\n")
    emails = to_emails + cc_emails + bcc_emails
 
    server = smtplib.SMTP(host)
    server.starttls()
    server.login(username, password)
    server.sendmail(from_addr, receivers, BODY)
    server.quit()
 
if __name__ == "__main__":
    receivers = ["xx1@domain.com","xx2@domain.com"]
    cc_emails = ["xx3@domain.com"]
    bcc_emails = ["xx4@domain.com"]
 
    subject = "puts your email subject here!"
    body_text = "puts your email content here!"
    send_email(subject, body_text, emails, cc_emails, bcc_emails)
    
'''config file looks as follow, username and password get from SMTP credentials:
server = email-smtp.us-east-1.amazonaws.com
from_addr = sender@domain.com
username = AKIxxx
password = Aqbxxxxxxxxxxxxxxxxxx
'''


