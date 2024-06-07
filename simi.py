import os
import re
from difflib import SequenceMatcher
from collections import defaultdict

# Function to find similarity ratio between two strings
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Function to group files by similarity
def group_files(files, threshold=0.2):
    groups = defaultdict(list)
    grouped = set()

    for i, file1 in enumerate(files):
        if file1 in grouped:
            continue
        groups[file1].append(file1)
        grouped.add(file1)

        for j, file2 in enumerate(files):
            if file2 not in grouped and similar(file1, file2) > threshold:
                groups[file1].append(file2)
                grouped.add(file2)

    return groups

# Get list of all .rar and .zip files in the current directory
current_dir = os.getcwd()
file_names = [f for f in os.listdir(current_dir) if f.endswith(('.rar', '.zip'))]

# Group files by similarity
file_groups = group_files(file_names)

# Create folders and move files
for group, files in file_groups.items():
    # Extract a folder name from the first file in the group
    folder_name = re.sub(r"[^A-Za-z0-9_]+", "_", group.split('.')[0])
    folder_path = os.path.join(current_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    for file in files:
        print(f"Moving {file} to {folder_name}/")
        source_path = os.path.join(current_dir, file)
        destination_path = os.path.join(folder_path, file)
        if os.path.exists(source_path):
            os.rename(source_path, destination_path)

# Print grouped results
for group, files in file_groups.items():
    print(f"Group: {group}")
    for file in files:
        print(f"  {file}")
