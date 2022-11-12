import sqlite3

connection = sqlite3.connect('/data/yellow/vineet/database/bi_multi_tables.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS popularity_table(
        name text primary key,
        date date,
        inst integer,
        vote integer,
        old integer,
        recent integer,
        no_files integer,
        maintainer text,
        inst_norm varchar,
        vote_norm varchar
        )""") 

connection.commit()
connection.close()
