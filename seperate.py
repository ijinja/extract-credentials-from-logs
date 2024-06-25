import os
import shutil
import zipfile
import rarfile
from concurrent.futures import ThreadPoolExecutor, as_completed

def is_zip_encrypted(zip_path):
    try:
        with zipfile.ZipFile(zip_path) as zf:
            for zinfo in zf.infolist():
                if zinfo.flag_bits & 0x1:
                    return True
            return False
    except Exception as e:
        print(f"Error checking ZIP file {zip_path}: {e}")
        return None  # None indicates an error occurred

def is_rar_encrypted(rar_path):
    try:
        with rarfile.RarFile(rar_path) as rf:
            for rinfo in rf.infolist():
                if rinfo.needs_password():
                    return True
            return False
    except rarfile.BadRarFile:
        print(f"Not a RAR file: {rar_path}")
        return None  # None indicates an error occurred
    except Exception as e:
        print(f"Error checking RAR file {rar_path}: {e}")
        return None  # None indicates an error occurred

def process_file(file_path):
    if file_path.lower().endswith('.zip'):
        encrypted = is_zip_encrypted(file_path)
        if encrypted is None:
            return None  # Skip file if an error occurred
        return (file_path, 'encrypted' if encrypted else 'non_encrypted')
    elif file_path.lower().endswith('.rar'):
        encrypted = is_rar_encrypted(file_path)
        if encrypted is None:
            return None  # Skip file if an error occurred
        return (file_path, 'encrypted' if encrypted else 'non_encrypted')
    return None

def separate_files():
    current_directory = os.getcwd()
    encrypted_dir = os.path.join(current_directory, 'encrypted')
    non_encrypted_dir = os.path.join(current_directory, 'non_encrypted')

    if not os.path.exists(encrypted_dir):
        os.makedirs(encrypted_dir)
    if not os.path.exists(non_encrypted_dir):
        os.makedirs(non_encrypted_dir)

    files = [os.path.join(current_directory, file) for file in os.listdir(current_directory) if os.path.isfile(os.path.join(current_directory, file))]
    zip_and_rar_files = [file for file in files if file.lower().endswith(('.zip', '.rar'))]

    with ThreadPoolExecutor() as executor:
        future_to_file = {executor.submit(process_file, file): file for file in zip_and_rar_files}
        for future in as_completed(future_to_file):
            result = future.result()
            if result:
                file_path, directory = result
                destination_dir = encrypted_dir if directory == 'encrypted' else non_encrypted_dir
                shutil.move(file_path, os.path.join(destination_dir, os.path.basename(file_path)))

if __name__ == "__main__":
    separate_files()
