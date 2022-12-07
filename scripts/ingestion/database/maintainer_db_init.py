#!/usr/bin/env python
import sqlite3
from scripts.ingestion.constants import DB_LOC

def target_con(con):
        conn = sqlite3.connect(con)
        cur = conn.cursor()
        return cur

def db_init():
        target_con(DB_LOC)
        cur.execute("""CREATE TABLE IF NOT EXISTS maintainer(
                name text primary key,
                inst integer,
                vote integer,
                old integer,
                recent integer,
                no_files integer
                )""") 

