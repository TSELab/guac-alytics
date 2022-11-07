#!/usr/bin/env python
import requests
import os.path
import re
import csv
import sqlite3

conn = sqlite3.connect('/data/yellow/vineet/database/bi_multi_tables.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS maintainer(
        name text primary key,
        inst integer,
        vote integer,
        old integer,
        recent integer,
        no_files integer
        )""") 


location = "https://popcon.debian.org/maint/by_inst"
target_filename = '/data/yellow/vineet/python_files/new_scripts/database_creation/maintainer.txt'
regex = "(\ )+"

def parse_line(line):
    # Header format
    # rank name inst vote old recent no-files
    rank, name, inst, vote, old, recent, no_files = \
        None, None, None, None, None, None, None
    line = line.strip()

    comma_divided = re.sub(regex, ",", line)
    comma_divided = comma_divided.split(",")
    rank = comma_divided[0]
    name = ' '.join(comma_divided[1:len(comma_divided)-5])
    inst, vote, old, recent, no_files = \
            [i for i in comma_divided[len(comma_divided)-5:]]
    
    return (rank, name, inst, vote, old, recent, no_files)

def main():
    if os.path.exists(target_filename):
        print("using local copy of the file")
    else:
        print("downloading file")
        response = requests.get(location)
        with open(target_filename, "wt") as fp:
            fp.write(response.text)

    with open(target_filename, "rt") as fp:
        data = fp.read()

    with open('/data/yellow/vineet/python_files/new_scripts/database_creation/maintainer.csv','w', encoding="utf-8",newline='') as fdout:
        wr = csv.DictWriter(fdout, fieldnames=['rank','name', 'inst', 'vote', 'old', 'recent', 'no_files'], extrasaction='ignore') 
        o=csv.writer(fdout)
        data = data.split("\n")
        for line in data[:len(data)-3]:
            if len(line) < 1 or line[0]=='#':
                continue
            line = parse_line(line)
            o.writerow(line)

    with open('/data/yellow/vineet/python_files/new_scripts/database_creation/maintainer.csv', 'r',encoding= 'unicode_escape') as file:
        data = csv.reader(file,delimiter=',')   
        no_records = 0 
        for row in data:
                n=row[1]
                i=row[2]
                v=row[3]
                o=row[4]
                r=row[5]
                no=row[6]
                # Inserting new values into the table 
                cur.execute('''INSERT OR REPLACE INTO maintainer VALUES (?,?,?,?,?,?)''',(n,i,v,o,r,no))
                conn.commit()
                no_records += 1
                

        print(no_records, ' checked')
        print('Closing file')

main()


       
