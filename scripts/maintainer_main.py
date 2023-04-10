#!/usr/bin/env python
import csv
from constants import MAINTAINER_CSV_FILE
from database.maintainer_db_init import db_init,conn,cur
from parsers.maintainer_parser import parser

def init():
    """ Inserting new values into the table """
    with open(MAINTAINER_CSV_FILE, 'r',encoding= 'unicode_escape') as file:
        data = csv.reader(file,delimiter=',')   
        no_records = 0 
        for row in data:
                n=row[1]
                i=row[2]
                v=row[3]
                o=row[4]
                r=row[5]
                no=row[6]
                cur.execute('''INSERT OR REPLACE INTO maintainer VALUES (?,?,?,?,?,?)''',(n,i,v,o,r,no))
                conn.commit()
                no_records += 1

        print(no_records, ' checked')
        print('Closing file')

if __name__ == "__main__":
        db_init() # Initialize the database
        parser() # Parse the data
        init() # Inserts the records into table

conn.close()
