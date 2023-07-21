import csv
from datetime import datetime
from ingestion.database.popcon_db_init import db_init,conn,cursor
from ingestion.constants import POPCON_CSV
from ingestion.parsers.popcon_parser import parser

no_records = 0  
def popcon():
        with open(POPCON_CSV, 'r',encoding= 'unicode_escape') as file:
                data = csv.reader(file,delimiter=',')   
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
                        conn.commit()
                        no_records += 1

if __name__ == "__main__":
        db_init()
        parser()
        popcon()
        
conn.close()
print ('\n{} records transferred'.format(no_records))  
