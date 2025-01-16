# KeySniffer

![mascot_racon.png](image\mascot_racon.png) 

---


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

1. **Download the Repository**:
   - If you have Git installed, you can clone the repository by running:
     ```bash
     git clone https://github.com/yourusername/KeySniffer.git
     ```
   - If you do not have Git installed, you can download the repository as a ZIP file:
     - Click the green **Code** button and select **Download ZIP**.
     - Extract the ZIP file to a directory of your choice.

2. **Install the Required Library**:
   - This script requires the `keyboard` library to capture keystrokes.
   - Install it by running the following command in your terminal:
     ```bash
     pip install keyboard
     ```

3. **Modify Email Configuration**:
   - Open `KeySniffer.py` and locate the email configuration section.
   - Replace the placeholder information with the sender and receiver email addresses.
   - Use an app-specific password for the sender email (see below for instructions).

4. **Create a Sender Email with App Password**:
   - Create a new email account.
   - Log into the Google account for the sender email.
   - Search for "App Passwords" in your account settings.
   - Create a new app-specific password (e.g., name it "Python").
   - Copy the generated password and paste it into the `KeySniffer.py` script. Ensure there are no spaces.

---

>[!NOTE]
>## Security Note
>**Do not use private email accounts or personal passwords for this project.** It is strongly advised to use a separate, dedicated email account created specifically for this purpose. Avoid using any credentials tied to your personal or professional accounts, as this could pose a significant security risk.

---

## License
This project is licensed under ***LICENSE***. See the LICENSE file for details.
