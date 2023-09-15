import csv
from datetime import datetime
from ingestion.database.popcon_db_init import db_init
from ingestion.constants import DB_LOC,POPCON_TEXT
from ingestion.parsers.popcon_parser import parser

def popcon(popcon_file):
        with open(popcon_file, 'r',encoding= 'unicode_escape') as file:
                data = csv.reader(file,delimiter=',')   
                x=datetime.now()
                no_records=0
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

        conn.close()
        print ('\n{} records transferred'.format(no_records))  

if __name__ == "__main__":
        popcon_file = parser(POPCON_TEXT) # Parse the data
        popcon_file = popcon_file.name
        conn,cursor = db_init(DB_LOC) # Initialize the database
        popcon(popcon_file) # Inserts the records into table
        
