#!/usr/bin/env python
import sqlite3
from scripts.ingestion.constants import *

def target_con(con):
        connection = sqlite3.connect(con)
        cursor = connection.cursor()
        return cursor

def db_init_main():
        target_con(constants.db_loc)
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

db_init_main()
connection.commit()
connection.close()
