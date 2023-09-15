#!/usr/bin/env python
import sqlite3
import sys
import os
# Get the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to the Python path
sys.path.append(parent_dir)
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