#!/usr/bin/env python
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
    server.login(from_addr, password)
    server.sendmail(from_addr, emails, BODY)
    server.quit()
 
if __name__ == "__main__":
    emails = ["xx@cyou-inc.com","xx2@cyou-inc.com"]
    cc_emails = ["xx3@cyou-inc.com","xx4@cyou-inc.com"]
    bcc_emails = ["xx5@cyou-inc.com","xx6@cyou-inc.com"]
 
    subject = "Test email from Python"
    body_text = "put your email body here"
    send_email(subject, body_text, emails, cc_emails, bcc_emails)
