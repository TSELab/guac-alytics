#!/usr/bin/env python
import csv
import sqlite3
from ingestion.constants import DB_LOC, MAINTAINER_TEXT_FILE
from ingestion.database.maintainer_db_init import db_init
from ingestion.parsers.maintainer_parser import parser

def init(maintainer_file):
    """ Inserting new values into the table """
    with open(maintainer_file, 'r',encoding= 'unicode_escape') as file:
        data = csv.reader(file,delimiter=',')   
        no_records = 0 
        for row in data:
                n=row[1]
                i=row[2]
                v=row[3]
                o=row[4]
                r=row[5]
                no=row[6]
                cursor.execute('''INSERT OR REPLACE INTO maintainer VALUES (?,?,?,?,?,?)''',(n,i,v,o,r,no))
                conn.commit()
                no_records += 1

        print(no_records, ' checked')
        print('Closing file')
        conn.close()

if __name__ == "__main__":
        maintainer_file = parser(MAINTAINER_TEXT_FILE) # Parse the data
        conn,cursor = db_init(DB_LOC) # Initialize the database
        init(maintainer_file) # Inserts the records into table
