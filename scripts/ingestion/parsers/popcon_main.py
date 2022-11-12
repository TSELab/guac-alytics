import csv
from datetime import datetime
import sqlite3

connection = sqlite3.connect('/data/yellow/vineet/database/bi_multi_tables.db')
cursor = connection.cursor()

with open('/data/yellow/vineet/python_files/new_scripts/data_pre_processing/today.csv', 'r',encoding= 'unicode_escape') as file:
        data = csv.reader(file,delimiter=',')   
        no_records = 0  
        x=datetime.now()
        for row in data:
                name=row[1]
                date="09/06/2022"
                inst=row[2]
                vote=row[3]
                old=row[4]
                recent=row[5]
                no_files=row[6]
                maintainer=row[7]
                cursor.execute('''INSERT OR REPLACE INTO popularity_table(name,date,inst,vote,old,recent,no_files,maintainer) VALUES (?,?,?,?,?,?,?,?)''',(name,date,inst,vote,old,recent,no_files,maintainer))
                connection.commit()
                no_records += 1

connection.close()
print ('\n{} records transferred'.format(no_records))  
