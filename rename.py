import os
import re

def rename_files_in_directory():
    # Get the current directory
    current_directory = os.getcwd()
    
    # Get all files in the current directory
    files = os.listdir(current_directory)
    
    # Set to keep track of existing filenames
    existing_filenames = set()

    for filename in files:
        # Match the pattern {number} - {anything}
        match = re.match(r'^(\d+) - (.+)$', filename)
        if match:
            # Extract the new name
            new_name = match.group(2)
            
            # Split new name to keep extension
            name, ext = os.path.splitext(new_name)
            
            # Handle duplicates
            original_name = name
            counter = 1
            while new_name in existing_filenames or os.path.exists(os.path.join(current_directory, new_name)):
                name = f"{original_name}_{counter}"
                new_name = name + ext
                counter += 1
            
            # Add the new name to the set of existing filenames
            existing_filenames.add(new_name)
            
            # Rename the file
            os.rename(os.path.join(current_directory, filename), os.path.join(current_directory, new_name))
            print(f"Renamed '{filename}' to '{new_name}'")

# Run the function
rename_files_in_directory()
