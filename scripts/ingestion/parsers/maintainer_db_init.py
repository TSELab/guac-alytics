#!/usr/bin/env python
import sqlite3

conn = sqlite3.connect('/data/yellow/vineet/database/bi_multi_tables.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS maintainer(
        name text primary key,
        inst integer,
        vote integer,
        old integer,
        recent integer,
        no_files integer
        )""") 

conn.commit()
conn.close()
