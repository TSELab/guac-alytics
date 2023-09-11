import re
import os

def get_file_path(folder_path):
  cpfile = None
  for root, dirs, files in os.walk(folder_path):
          for file in files:
              if file.lower().startswith("copyright"):
                cpfile = os.path.join(root, file)
                
  return cpfile

def get_license(folder_path):
  file_path = get_file_path(folder_path)
  if file_path:
    with open(file_path, "r", encoding="utf-8", errors='ignore') as file:
      text = file.read()
    # Split the text into individual sections using 'Files: ' as a delimiter
      sections = re.split(r'\nFiles: ', text.strip())

      # Initialize a dictionary to store file and license information
      files_and_licenses = {}

      # Iterate through the sections and extract file and license information
      for section in sections[1:]:  # Skip the first empty section
            lines = section.strip().split('\n')
            file_pattern = lines[0]
            license_match = re.search(r'License: (.+)', section)
            
            if license_match:
                license_pattern = license_match.group(1)
                # Add the file and license information to the dictionary
                files_and_licenses[file_pattern] = license_pattern

    # Print the resulting dictionary
      return files_and_licenses
  return None
  
# a = get_license("/data/yellow/guacalytics/raw_data/upstream_clones/clone_repos/menhir")
# print(a)
