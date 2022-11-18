#!/usr/bin/env python
import csv
import sqlite3

conn = sqlite3.connect('/data/yellow/vineet/database/bi_multi_tables.db')
cur = conn.cursor()

def main():
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
conn.close()
