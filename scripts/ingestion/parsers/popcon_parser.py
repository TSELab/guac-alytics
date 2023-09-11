#!/usr/bin/env python
import requests
import os
import re
import csv
from datetime import datetime
from constants import INST_LOC,POPCON_TEXT,POPCON_CSV, REGEX

x=datetime.now()
        
def parse_line(line):
    # Parse each line and return the values
    rank, name, inst, vote, old, recent, no_files, maintainer = \
        None, None, None, None, None, None, None, None

    line = line.strip()
    # Extract the maintainer from the line
    try:
        rest, maintainer = line.split("(")
        maintainer = maintainer.replace(")","") # Replace 
    except Exception as e:
        print(line)
        print(e)

    # Replace separator in line with commas
    comma_divided = re.sub(REGEX, ",", rest)
    rank, name, inst, vote, old, recent, no_files, _ = \
            comma_divided.split(",")

    return (rank, name, inst, vote, old, recent, no_files, maintainer)

def parser(textfile=POPCON_TEXT):
    # Check if local copy of file exists, otherwise download
    if os.path.exists(textfile):
        print("using local copy of the file")
    else:
        print("downloading file")
        response = requests.get(INST_LOC)
        with open(textfile, "wt") as fp:
            fp.write(response.text)

    with open(textfile, "rt") as fp:
        data = fp.read()

    with open(POPCON_CSV,'w', encoding="utf-8",newline='') as fdout:
            wr=csv.writer(fdout)
            data = data.split("\n")
            for line in data[:len(data)-3]:
                
                # Skip empty or commented lines
                if len(line) < 1 or line[0]=='#':
                    continue
                line = parse_line(line)
                wr.writerow(line)    

    fp.close()
    fdout.close()
    os.remove(textfile)
    file = open(POPCON_CSV, "r")
    return file


