#!/usr/bin/env python
import requests
import os.path
import re
import csv
from constants import REGEX, MAINTAINER_TEXT_FILE, MAINTAINER_CSV_FILE, MAINTAINER_INST_LOC

# Define the function to parse each line of the file
def parse_line(line):
    # Initialize variables
    rank, name, inst, vote, old, recent, no_files = None, None, None, None, None, None, None
    
    # Remove extra spaces and replace semicolons with commas
    line = line.strip()
    line = re.sub(REGEX, ",", line)
    
    # Split the line into its components
    components = line.split(",")
    
    # Extract the relevant information
    rank = components[0]
    name = ' '.join(components[1:-5])
    inst, vote, old, recent, no_files = components[-5:]
    
    return (rank, name, inst, vote, old, recent, no_files)

# Define the main parser function
def parser(textfile = MAINTAINER_TEXT_FILE):
    # Check if the file exists locally, if not, download it
    if os.path.exists(textfile):
        print("Using local copy of the file.")
    else:
        print("Downloading file.")
        response = requests.get(MAINTAINER_INST_LOC)
        with open(textfile, "wt") as fp:
            fp.write(response.text)

    # Read the file and convert it to a CSV format
    with open(textfile, "rt") as fp, open(MAINTAINER_CSV_FILE,'w', encoding="utf-8",newline='') as fdout:
        # Initialize the CSV writer and write the header row
        wr = csv.DictWriter(fdout, fieldnames=['rank','name', 'inst', 'vote', 'old', 'recent', 'no_files'], extrasaction='ignore')
        wr.writeheader()
        
        # Loop through the lines in the file and write them to the CSV file
        for line in fp:
            # Skip empty lines and lines starting with #
            if not line.strip() or line.startswith("#"):
                continue
            
            # Parse the line and write it to the CSV file
            parsed_line = parse_line(line)
            wr.writerow(dict(zip(['rank','name', 'inst', 'vote', 'old', 'recent', 'no_files'], parsed_line)))

    fp.close()
    fdout.close()
    os.remove(textfile)
    file = open(MAINTAINER_CSV_FILE, "r")
    return file