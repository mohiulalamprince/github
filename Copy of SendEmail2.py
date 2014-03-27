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

def mail(to, subject, text, attach1):
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
   
   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()

while (True):

   

   inFile = open('totalCrawlingStatisic.info', 'r')
   #outFile = open('Find-saFormatedHostList.txt', 'w')

   for line in inFile.readlines():
       line = line.strip()
       totalURL = line.split('#')[0]
       totalDownloaded = line.split('#')[1]
       totalError = line.split('#')[2]

       status = "PLEASE READ THE CRAWLER STATUS\n" + "TOTAL_URL="+totalURL+"\nTOTAL_DOWNLOADED="+totalDownloaded+"\nTOTAL_ERROR="+totalError+"\n"
       
   inFile.close()
   
    mail("maprince@gmail.com",
       "WebCrawler Status Email",
       status, "finishHostList.txt")
    time.sleep(60)