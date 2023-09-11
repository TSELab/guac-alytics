#!/usr/bin/env python
from constants import DB_LOC
import sqlite3

def db_init(location=DB_LOC):
        conn = sqlite3.connect(location)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS maintainer(
                name text primary key,
                inst integer,
                vote integer,
                old integer,
                recent integer,
                no_files integer
                )""") 
        return conn,cursor
