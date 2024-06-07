import os
import patoolib
import shutil

def decompress_file(archive_path, password):
    """Extract only 'passwords.txt' from the archive using the given password."""
    try:
        extract_dir = os.path.join(os.path.dirname(archive_path), 'temp_extract')
        os.makedirs(extract_dir, exist_ok=True)
        
        # Attempt to extract the archive
        patoolib.extract_archive(archive_path, outdir=extract_dir, password=password)
        
        # Check for 'passwords.txt' and move to 'extracted' if found
        extracted_file = os.path.join(extract_dir, 'passwords.txt')
        if os.path.exists(extracted_file):
            shutil.move(extracted_file, os.path.join('extracted', os.path.basename(archive_path) + '_passwords.txt'))
            return True
        else:
            return False
    except patoolib.util.PatoolError:
        return False
    finally:
        shutil.rmtree(extract_dir, ignore_errors=True)

def process_archives(folder_path, password_file_name, failed_folder_name):
    """Process all the archives in the given folder, using passwords from the password file."""
    # Ensure required folders exist
    os.makedirs('extracted', exist_ok=True)
    os.makedirs(failed_folder_name, exist_ok=True)

    # Construct the path to the password file
    password_file = os.path.join(folder_path, password_file_name)

    # Load passwords from the file
    with open(password_file, 'r',encoding='utf-8') as pf:
        passwords = pf.read().splitlines()

    # Process all archives in the folder
    print('heer')
    for file in os.listdir(folder_path):
        if file.endswith(('.rar', '.zip')):  # Add more formats if needed
            archive_path = os.path.join(folder_path, file)
            print(f"Processing {file}...")
            success = False

            for password in passwords:
                if decompress_file(archive_path, password):
                    print(f"Successfully extracted 'passwords.txt' from {file} with password: {password}")
                    os.remove(archive_path)  # Delete the archive file
                    success = True
                    break

            if not success:
                print(f"Failed to extract 'passwords.txt' from {file}, moving to {failed_folder_name}.")
                shutil.move(archive_path, os.path.join(failed_folder_name, file))

# Example usage
folder_path = os.getcwd()  # Set to the current directory
password_file_name = 'pass.txt'  # Set to your password file name
failed_folder_name = 'failed_folder'  # Set the name of the failed folder
process_archives(folder_path, password_file_name, failed_folder_name)
