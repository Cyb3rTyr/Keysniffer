# KeySniffer

>[!Warning]
>## Disclaimer
>This material is strictly for educational and research purposes. Any misuse, distribution, or deployment of malware for malicious intent is illegal and unethical. Always operate in secure, controlled environments, and comply with all relevant laws and regulations.
>
>**I am not responsible for any actions taken by others with this material. Use it responsibly and at your own risk.**

---

## About the Project
KeySniffer is a Python-based keylogger designed to demonstrate how keystroke logging works. It captures and filters input to identify specific patterns of valuable information. 

This project was developed as part of a school assignment and is intended solely for educational purposes.

---

## Features
The script identifies and records the following types of information:
- Phone numbers (e.g., +352 123 123 123)
- Email addresses
- URLs (HTTP and HTTPS)
- Credit card details
- Dates
- IP addresses (IPv4 and IPv6)

---

## Setup and Usage

1. **Modify Email Configuration**:
   - Open `KeySniffer.py` and locate the email configuration section.
   - Replace the placeholder information with the sender and receiver email addresses.
   - Use an app-specific password for the sender email (see below for instructions).

2. **Create a Sender Email with App Password**:
   - Create a new email account.
   - Log into the Google account for the sender email.
   - Search for "App Passwords" in your account settings.
   - Create a new app-specific password (e.g., name it "Python").
   - Copy the generated password and paste it into the `KeySniffer.py` script. Ensure there are no spaces.

---

## Security Note
Avoid storing passwords in plain text. Use environment variables or a secure secrets manager to protect sensitive information.

---

## License
This project is licensed under [Your License]. See the LICENSE file for details.
