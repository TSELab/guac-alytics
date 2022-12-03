import csv
from datetime import datetime
import sqlite3
from scripts.ingestion.database.popcon_db_init import db_init_main

def popcon():
        with open('/data/yellow/vineet/python_files/new_scripts/data_pre_processing/today.csv', 'r',encoding= 'unicode_escape') as file:
                data = csv.reader(file,delimiter=',')   
                no_records = 0  
                x=datetime.now()
                for row in data:
                        name=row[1]
                        date=x
                        inst=row[2]
                        vote=row[3]
                        old=row[4]
                        recent=row[5]
                        no_files=row[6]
                        maintainer=row[7]
                        cursor.execute('''INSERT OR REPLACE INTO popularity_table(name,date,inst,vote,old,recent,no_files,maintainer) VALUES (?,?,?,?,?,?,?,?)''',(name,date,inst,vote,old,recent,no_files,maintainer))
                        connection.commit()
                        no_records += 1

if __name__ == "__main__":
        db_init_main()
        popcon()
        
connection.close()
print ('\n{} records transferred'.format(no_records))  
