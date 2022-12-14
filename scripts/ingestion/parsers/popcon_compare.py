import csv
from curses import noraw
from datetime import date, datetime
import sqlite3
from bs4 import BeautifulSoup as bs 
import requests
import csv
import os
import shutil

x=datetime.now()
print('On ', datetime.strftime(x,"%m/%d/%Y"))

# Connecting to database
conn = sqlite3.connect('/data/yellow/vineet/database/bi_multi_tables.db')
cur = conn.cursor()

# Getting data from popularity contest
url = 'https://popcon.debian.org/by_inst'

page = requests.get(url)

data = bs(page.content,"html.parser")
data = str(data)

# Splitting the data to store in a text file
if ('\n\n') in data:
        data = data.split('\n')[1]
else:
        data = data


# Getting statistics of debian architecture
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

# Storing the popularity contest values in a text file
with open('/data/yellow/vineet/python_files/new_scripts/data_pre_processing/today.txt', 'w', encoding="utf-8") as fdin:
        fdin.write(data)
        print("Downloaded Data")
    
fdin.close()
totinst=282358448

# Copying the data from text file to csv 
with open('/data/yellow/vineet/python_files/new_scripts/data_pre_processing/today.txt', 'r', encoding="utf-8") as fdin, open('/data/yellow/vineet/python_files/new_scripts/data_pre_processing/today.csv','w', encoding="utf-8",newline='') as fdout:
        wr = csv.DictWriter(fdout, fieldnames=['sno','Name', 'inst', 'vote', 'old', 'recent', 'no_files', 'maintainer'], extrasaction='ignore')  # ignore unwanted fields 
        o=csv.writer(fdout)
        for line in fdin:
                # print("line is",line)
                # print(type(line))
                if not ('#' or '----' or 'Total' or '</') in line:
                        o.writerow(line.split(None,7))

fdin.close()
fdout.close()
os.remove('/data/yellow/vineet/python_files/new_scripts/data_pre_processing/today.txt')   

year=date.today().year
mon=date.today().month
day=date.today().day

# Saving data of each day
shutil.copyfile('/data/yellow/vineet/python_files/new_scripts/data_pre_processing/today.csv','/data/yellow/vineet/raw_data/popularity_contest/{}/{}/{}'.format(year,mon,day))

# Comparing the data from csv file and existing table and updating its values 
with open('/data/yellow/vineet/python_files/new_scripts/data_pre_processing/today.csv', 'r',encoding= 'unicode_escape') as file:
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
            cur.execute('''UPDATE popularity_table SET date=(?) WHERE name=(?) and vote!=(?)''',(y,n,v))  
            cur.execute(''' UPDATE popularity_table SET inst=(?), vote=(?), old=(?), recent=(?), no_files=(?), inst_norm=(?), vote_norm=(?) WHERE name=(?)''', (i,v,o,r,no,ia,va,n))          
            # Inserting new values into the table 
            cur.execute('''INSERT OR REPLACE INTO popularity_table VALUES (?,?,?,?,?,?,?,?,?,?)''',(n,y,i,v,o,r,no,maintainer,ia,va))
            conn.commit()
            no_records += 1
            if(no_records%25000==0):
                print(no_records, ' checked')

print('Closing file')
file.close()
os.remove('/data/yellow/vineet/python_files/new_scripts/data_pre_processing/today.csv')
conn.close()
