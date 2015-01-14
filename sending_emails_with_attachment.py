#!/usr/bin/env python
import os, sys
import smtplib
import string
 
from configobj import ConfigObj
from email import Encoders
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.Utils import formatdate

def send_email_with_attachment(subject, body_text, to_emails, cc_emails, bcc_emails, file_to_attach):
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "config.ini")
    header = 'Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file_to_attach)
 
    # get the config
    if os.path.exists(config_path):
        cfg = ConfigObj(config_path)
        cfg_dict = cfg.dict()
    else:
        print "Config not found! Exiting!"
        sys.exit(1)
 
    # extract server and from_addr from config
    host = cfg_dict["server"]
    from_addr = cfg_dict["from_addr"]
    password = cfg_dict["password"]
 
    # create the message
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    if body_text:
        msg.attach( MIMEText(body_text) )
 
    msg["To"] = ', '.join(to_emails)
    msg["cc"] = ', '.join(cc_emails)
 
    attachment = MIMEBase('application', "octet-stream")
    try:
        with open(file_to_attach, "rb") as fh:
            data = fh.read()
        attachment.set_payload( data )
        Encoders.encode_base64(attachment)
        attachment.add_header(*header)
        msg.attach(attachment)
    except IOError:
        msg = "Error opening attachment file %s" % file_to_attach
        print msg
        sys.exit(1)
 
    emails = to_emails + cc_emails
 
    server = smtplib.SMTP(host)
    server.login(from_addr, password)
    server.sendmail(from_addr, emails, msg.as_string())
    server.quit()
 
if __name__ == "__main__":
    emails = ["xx@cyou-inc.com"]
    cc_emails = ["xx@cyou-inc.com"]
    bcc_emails = ["xx@cyou-inc.com"]
 
    subject = "Test email with attachment from Python"
    attchment = os.sys.path[0] + os.sep + 'file_name'
#    body_text = "This email contains an attachment!"
    f = open(attchment,'r')
    body_text = f.read()
    f.close()
    send_email_with_attachment(subject, body_text, emails, 
                               cc_emails, bcc_emails, attchment)
