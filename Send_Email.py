import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'xxxx@outlook.com'
PASSWORD = 'xxxxxxx'

def main():
    names = 'Philip'
    emails = 'xxxxx@outlook.com'

    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()


    msg['From']=MY_ADDRESS
    msg['To']=emails
    msg['Subject']='[Important]'
    msg.preamble='[Important]'
        
    with open('test_message.txt', 'r') as msg_file:
        msg.attach(MIMEText(msg_file.read()))

    print msg
 
    s.sendmail('xxxx@outlook.com', 'xxxxx@outlook.com', msg.as_string())
    del msg
        
    s.quit()
