import os
import re

def search_files(directory, pattern):
    matches = []
    
    for root, _, files in os.walk(directory):
        for file_name in files:
            if 'pass' in file_name.lower() and file_name.lower().endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                    found_matches = re.findall(pattern, content)
                    if found_matches:
                        matches.append((file_path, found_matches))
    
    return matches

def find_non_matching_files(directory, *patterns):
    non_matching_files = []
    
    for root, _, files in os.walk(directory):
        for file_name in files:
            if 'pass' in file_name.lower() and file_name.lower().endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                    found_matches = [re.findall(pattern, content) for pattern in patterns]
                    if not any(found_matches):
                        non_matching_files.append(file_path)
    
    return non_matching_files

directory_to_search = "."
patterns_to_search = [
    r"URL:\s*(.*?)\n.*?Username:\s*(.*?)\n.*?Password:\s*(.*?)\n",
    r"Host:\s*(.*?)\n.*?Login:\s*(.*?)\n.*?Password:\s*(.*?)\n",
    r"URL:\s*(.*?)\n.*?USER:\s*(.*?)\n.*?PASS:\s*(.*?)\n",
    r"url:\s*(.*?)\n.*?login:\s*(.*?)\n.*?password:\s*(.*?)\n",
    r"URL:\s*(.*?)\n.*?Login:\s*(.*?)\n.*?Password:\s*(.*?)\n",
    r"URL :\s*(.*?)\n.*?Username :\s*(.*?)\n.*?Password :\s*(.*?)\n",
    r"Host : \s*(.*?)\n.*?Login : \s*(.*?)\n.*?Password : \s*(.*?)\n",
   r"Url: \s*(.*?)\n.*?Login: \s*(.*?)\n.*?Password: \s*(.*?)\n"

]

results = [search_files(directory_to_search, pattern) for pattern in patterns_to_search]

with open("credentials.txt", "w", encoding="utf-8", errors="ignore") as output_file:
    for result in results:
        for path, matches in result:
            for match in matches:
                url, username, password = (item.strip() for item in match)
                credential_line = f"{url}:{username}:{password}\n"
                output_file.write(credential_line)

non_matching_files = find_non_matching_files(directory_to_search, *patterns_to_search)

with open("non_matching_files.txt", "w", encoding="utf-8", errors="ignore") as output_file:
    for file_path in non_matching_files:
        output_file.write(f"{file_path}\n")

def remove_duplicates(file_path):
    lines_seen = set()
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        lines = file.readlines()
    with open(file_path, "w", encoding="utf-8", errors="ignore") as output_file:
        for line in lines:
            if line not in lines_seen:
                output_file.write(line)
                lines_seen.add(line)

remove_duplicates("credentials.txt")
