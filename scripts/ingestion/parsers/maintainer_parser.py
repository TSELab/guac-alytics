#!/usr/bin/env python
import requests
import os.path
import re
import csv
from scripts.ingestion.constants import REGEX,MAINTAINER_TEXT_FILE,MAINTAINER_CSV_FILE,MAINTAINER_INST_LOC
from scripts.ingestion.database.maintainer_db_init import db_init

def parse_line(line):
    # Header format
    # rank name inst vote old recent no-files
    rank, name, inst, vote, old, recent, no_files = \
        None, None, None, None, None, None, None
    line = line.strip()

    comma_divided = re.sub(constants.REGEX, ",", line)
    comma_divided = comma_divided.split(",")
    rank = comma_divided[0]
    name = ' '.join(comma_divided[1:len(comma_divided)-5])
    inst, vote, old, recent, no_files = \
            [i for i in comma_divided[len(comma_divided)-5:]]
    
    return (rank, name, inst, vote, old, recent, no_files)

def parser():
    if os.path.exists(constants.MAINTAINER_TEXT_FILE):
        print("using local copy of the file")
    else:
        print("downloading file")
        response = requests.get(constants.MAINTAINER_INST_LOC)
        with open(constants.MAINTAINER_TEXT_FILE, "wt") as fp:
            fp.write(response.text)

    with open(constants.MAINTAINER_TEXT_FILE, "rt") as fp:
        data = fp.read()

    with open(constants.MAINTAINER_CSV_FILE,'w', encoding="utf-8",newline='') as fdout:
        wr = csv.DictWriter(fdout, fieldnames=['rank','name', 'inst', 'vote', 'old', 'recent', 'no_files'], extrasaction='ignore')  # ignore unwanted fields 
        o=csv.writer(fdout)
        data = data.split("\n")
        for line in data[:len(data)-3]:
            if len(line) < 1 or line[0]=='#':
                continue
            line = parse_line(line)
            o.writerow(line)

if __name__ == "__main__":
    db_init()
    parser()
