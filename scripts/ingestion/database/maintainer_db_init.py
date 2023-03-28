#!/usr/bin/env python
import sqlite3
from constants import DB_LOC

conn = sqlite3.connect(DB_LOC)
cur = conn.cursor()

def db_init():
        cur.execute("""CREATE TABLE IF NOT EXISTS maintainer(
                name text primary key,
                inst integer,
                vote integer,
                old integer,
                recent integer,
                no_files integer
                )""") 

