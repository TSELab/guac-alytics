#!/usr/bin/env python
import sqlite3
from scripts.ingestion.constants import *

def target_con(con):
        conn = sqlite3.connect(con)
        cur = conn.cursor()
        return cur

def db_init_main():
        target_con(constants.db_loc)
        cur.execute("""CREATE TABLE IF NOT EXISTS maintainer(
                name text primary key,
                inst integer,
                vote integer,
                old integer,
                recent integer,
                no_files integer
                )""") 

db_init_main()
conn.commit()
conn.close()
