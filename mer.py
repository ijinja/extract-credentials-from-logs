import os

def merge_files_in_directories():
    current_directory = os.getcwd()

    for dir_name in os.listdir(current_directory):
        dir_path = os.path.join(current_directory, dir_name)
        
        if os.path.isdir(dir_path):
            files = os.listdir(dir_path)
            
            # Only process directories with one or two files
            if 1 <= len(files) <= 2:
                merged_content = ""
                for file_name in files:
                    file_path = os.path.join(dir_path, file_name)
                    
                    if os.path.isfile(file_path):
                        with open(file_path, 'r', encoding='utf-8') as file:
                            merged_content += file.read() + "\n"

                # Write the merged content to a new file
                merged_file_path = os.path.join(dir_path, "merged_file.txt")
                with open(merged_file_path, 'w', encoding='utf-8') as merged_file:
                    merged_file.write(merged_content.strip())
                
                print(f"Merged files in '{dir_name}' into '{merged_file_path}'")

# Run the function
merge_files_in_directories()
