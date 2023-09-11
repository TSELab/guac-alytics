#!/usr/bin/env python
import sqlite3
from constants import DB_LOC

def db_init(location=DB_LOC):
        conn = sqlite3.connect(location)
        cursor = conn.cursor()
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

        return conn,cursor