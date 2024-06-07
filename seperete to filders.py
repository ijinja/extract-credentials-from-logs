import os
import shutil

# Get the current directory
current_dir = os.getcwd()

# Get a list of all files in the current directory
files = os.listdir(current_dir)

# Create a counter to keep track of the current folder number
folder_num = 1

# Iterate through the files
for i, file in enumerate(files):
    # Check if the file is a directory (we don't want to move directories)
    if os.path.isdir(os.path.join(current_dir, file)):
        continue

    # Create the folder name
    folder_name = f"folder_{folder_num}"

    # Create the folder if it doesn't already exist
    folder_path = os.path.join(current_dir, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Move the file to the folder
    src_path = os.path.join(current_dir, file)
    dst_path = os.path.join(folder_path, file)
    shutil.move(src_path, dst_path)

    # Increment the folder number if we've reached 10 files
    if (i + 1) % 10 == 0:
        folder_num += 1

print("Files have been separated into folders.")
