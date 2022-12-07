import csv
from datetime import datetime
import sqlite3
from scripts.ingestion.database.popcon_db_init import db_init
from scripts.ingestion.constants import POPCON_CSV
from scripts.ingestion.parsers.popcon_parser import parser

def popcon():
        with open(POPCON_CSV, 'r',encoding= 'unicode_escape') as file:
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
                        cur.execute('''INSERT OR REPLACE INTO popularity_table(name,date,inst,vote,old,recent,no_files,maintainer) VALUES (?,?,?,?,?,?,?,?)''',(name,date,inst,vote,old,recent,no_files,maintainer))
                        conn.commit()
                        no_records += 1

if __name__ == "__main__":
        db_init()
        parser()
        popcon()
        
conn.close()
print ('\n{} records transferred'.format(no_records))  
