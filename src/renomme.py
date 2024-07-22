import os
import re

def atoi(text):
    return int(text) if text.isdigit() else text.lower()

def natural_keys(s):
    return [atoi(text) for text in re.split(r'(\d+)', s)]  # Use raw string for regex

def rename_files_in_order(directory):
    files = os.listdir(directory)
    files.sort(key=natural_keys)

    for i, filename in enumerate(files):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            new_filename = f"{i+1:03d}_{filename}"
            new_file_path = os.path.join(directory, new_filename)
            os.rename(file_path, new_file_path)
            print(f"Renamed '{filename}' to '{new_filename}'")

directory_path = r'10k'  # Update this path
rename_files_in_order(directory_path)
