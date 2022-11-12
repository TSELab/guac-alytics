import csv
from curses import noraw
from datetime import date, datetime
from bs4 import BeautifulSoup as bs 
import requests
import csv
import os
import shutil

x=datetime.now()
print('On ', datetime.strftime(x,"%m/%d/%Y"))


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


# Storing the popularity contest values in a text file
with open('/data/yellow/vineet/python_files/new_scripts/data_pre_processing/today.txt', 'w', encoding="utf-8") as fdin:
        fdin.write(data)
        print("Downloaded Data")
    
fdin.close()

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
