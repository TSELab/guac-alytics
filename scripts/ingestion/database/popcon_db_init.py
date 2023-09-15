#!/usr/bin/env python
import sqlite3
import sys
import os
# Get the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # Go up two levels to the project root

# Add the project root directory to sys.path
sys.path.append(parent_dir)
from ingestion import constants
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