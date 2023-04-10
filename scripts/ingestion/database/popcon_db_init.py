#!/usr/bin/env python
import sqlite3
from constants import DB_LOC

conn = sqlite3.connect(DB_LOC)
cursor = conn.cursor()

def db_init():
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
