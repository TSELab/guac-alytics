#!/usr/bin/env python
import requests
import os.path
import re
import csv
import shutil
from bs4 import BeautifulSoup as bs 
from datetime import datetime,date
from ..constants import POPCON_CSV,POPCON_TEXT,INST_LOC,DB_LOC,REGEX
from database.popcon_db_init import target_con,conn,cursor

x=datetime.now()
print('On ', datetime.strftime(x,"%m/%d/%Y"))

#Connecting to database
target_con(DB_LOC)

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
    url1 = 'https://popcon.debian.org'
    page1 = requests.get(url1)
    data1 = bs(page1.content,"html.parser")
    value = data1.find('td',class_='stats-cell')
    d = str(value)
    if (":") in d:
            d = d.split()
    else:
            d = d               
    amd=(int(d[14]))
    print("The amd64 is ",amd)
    l=0
    j=0
    for i in d:
            if((j%7==0 and j!=0 and j!=189) or j==187):
                    #print(j,i)
                    l+=int(i)
            j+=1
            
    print("Final value is ",l)

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


    fp.close()
    fdout.close()
    os.remove(POPCON_TEXT)   

    year=date.today().year
    mon=date.today().month
    day=date.today().day

    # Saving data of each day
    shutil.copyfile(POPCON_CSV,'/data/yellow/vineet/raw_data/popularity_contest/{}/{}/{}'.format(year,mon,day))

    # Comparing the data from csv file and existing table and updating its values 
    with open(POPCON_CSV, 'r',encoding= 'unicode_escape') as file:
            data = csv.reader(file,delimiter=',')   
            no_records = 0 
            nor=amd/l
            for row in data:
                n=row[1]
                i=row[2]
                v=row[3]
                o=row[4]
                r=row[5]
                no=row[6]
                ia=(float(row[2])*nor)
                va=(float(row[3])*nor)
                maintainer=row[7]
                y=datetime.strftime(x,"%m/%d/%Y")
                # Updating the date if the number of votes of the package is changed
                cursor.execute('''UPDATE popularity_table SET date=(?) WHERE name=(?) and vote!=(?)''',(y,n,v))  
                cursor.execute(''' UPDATE popularity_table SET inst=(?), vote=(?), old=(?), recent=(?), no_files=(?), inst_norm=(?), vote_norm=(?) WHERE name=(?)''', (i,v,o,r,no,ia,va,n))          
                # Inserting new values into the table 
                cursor.execute('''INSERT OR REPLACE INTO popularity_table VALUES (?,?,?,?,?,?,?,?,?,?)''',(n,y,i,v,o,r,no,maintainer,ia,va))
                conn.commit()
                no_records += 1
                if(no_records%25000==0):
                    print(no_records, ' checked')

    print('Closing file')
    file.close()
    os.remove(POPCON_CSV)
    conn.close()
        
parser()
