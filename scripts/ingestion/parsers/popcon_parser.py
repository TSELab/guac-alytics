#!/usr/bin/env python
import requests
import os
import re
import csv
from scripts.ingestion.constants import INST_LOC,POPCON_TEXT,POPCON_CSV

x=datetime.now()
        
def parse_line(line):
    # Header format
    # rank name inst vote old recent no-files (maintainer)
    rank, name, inst, vote, old, recent, no_files, maintainer = \
        None, None, None, None, None, None, None, None

    line = line.strip()
    # print(line)
    try:
        rest, maintainer = line.split("(")
        maintainer = maintainer.replace(")","") # Replace 
    except Exception as e:
        print(line)
        print(e)

    
    comma_divided = re.sub(REGEX, ",", rest)
    rank, name, inst, vote, old, recent, no_files, _ = \
            comma_divided.split(",")
    # print(maintainer)
    return (rank, name, inst, vote, old, recent, no_files, maintainer)

def parser():
    if os.path.exists(POPCON_TEXT):
        print("using local copy of the file")
    else:
        print("downloading file")
        response = requests.get(INST_LOC)
        with open(POPCON_TEXT, "wt") as fp:
            fp.write(response.text)

    with open(POPCON_TEXT, "rt") as fp:
        data = fp.read()

    with open(POPCON_CSV,'w', encoding="utf-8",newline='') as fdout:
            wr = csv.DictWriter(fdout, fieldnames=['sno','Name', 'inst', 'vote', 'old', 'recent', 'no_files', 'maintainer'], extrasaction='ignore')  # ignore unwanted fields 
            o=csv.writer(fdout)
            data = data.split("\n")
            for line in data[:len(data)-3]:
                if len(line) < 1 or line[0]=='#':
                    continue
                line = parse_line(line)
                o.writerow(line)    



