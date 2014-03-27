#!/usr/bin/python

import smtplib
import time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

gmail_user = "maprince@gmail.com"
gmail_pwd = "042162071"

def mail(to, subject, text, attach1, attach2, attach3, attach4, attach5, attach6, attach7, attach8, attach9, attach10, attach11, attach12):
   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach1, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach1))
   msg.attach(part)
   
   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach2, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach2))
   msg.attach(part)

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach3, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach3))
   msg.attach(part)

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach4, 'rb').read())
   Encoders.encode_base64(part)   
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach4))
   msg.attach(part)

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach5, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach5))
   msg.attach(part)

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach6, 'rb').read())
   Encoders.encode_base64(part)   
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach6))
   msg.attach(part)

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach7, 'rb').read())
   Encoders.encode_base64(part)   
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach7))
   msg.attach(part)

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach8, 'rb').read())
   Encoders.encode_base64(part)   
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach8))
   msg.attach(part)

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach9, 'rb').read())
   Encoders.encode_base64(part)   
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach9))
   msg.attach(part)

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach10, 'rb').read())
   Encoders.encode_base64(part)   
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach10))
   msg.attach(part)

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach12, 'rb').read())
   Encoders.encode_base64(part)   
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach11))
   msg.attach(part)

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach1, 'rb').read())
   Encoders.encode_base64(part)   
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach12))
   msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()

while (True):
    mail("maprince@gmail.com",
       "WebCrawler Status Email",
       "Please read the Web Crawler Status attachment",
       "activeHost.info",
         "CrawlerLog.CM",
         "CrawlerStatistics.CM",
         "crawlingLogFile.info",
         "errorInfo.CM",
         "errorInfo.CONF",
         "finishedHostFile.info",
         "finishHostList.txt",
         "info.CM",
         "RecentHostList.info",
         "RecentHostList.txt",
         "totalCrawlingStatisic.info")
    time.sleep(60)