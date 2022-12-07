import csv
from curses import noraw
from datetime import date, datetime
from bs4 import BeautifulSoup as bs 
import requests
import csv
import os
import shutil
from scripts.ingestion.constants import INST_LOC,POPCON_TEXT,POPCON_CSV

x=datetime.now()

def parser():
        print('On ', datetime.strftime(x,"%m/%d/%Y"))
        # Getting data from popularity contest
        page = requests.get(INST_LOC)

        data = bs(page.content,"html.parser")
        data = str(data)

        # Splitting the data to store in a text file
        if ('\n\n') in data:
                data = data.split('\n')[1]
        else:
                data = data
                
        # Storing the popularity contest values in a text file
        with open(POPCON_TEXT, 'w', encoding="utf-8") as fdin:
                fdin.write(data)
                print("Downloaded Data")
        
        fdin.close()

        # Copying the data from text file to csv 
        with open(POPCON_TEXT, 'r', encoding="utf-8") as fdin, open(POPCON_CSV,'w', encoding="utf-8",newline='') as fdout:
                wr = csv.DictWriter(fdout, fieldnames=['sno','Name', 'inst', 'vote', 'old', 'recent', 'no_files', 'maintainer'], extrasaction='ignore')  # ignore unwanted fields 
                o=csv.writer(fdout)
                for line in fdin:
                        # print("line is",line)
                        # print(type(line))
                        if not ('#' or '----' or 'Total' or '</') in line:
                                o.writerow(line.split(None,7))

        fdin.close()
        fdout.close()
        os.remove(POPCON_TEXT)



