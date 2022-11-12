#!/usr/bin/env python
import sqlite3

conn = sqlite3.connect('/data/yellow/vineet/database/bi_multi_tables.db')
cur = conn.cursor()

# Creating table 
cur.execute("""CREATE TABLE IF NOT EXISTS buildinfo_data (
       source varchar,
       version varchar,
       arch varchar,
       time datetime,
       deps varchar)""")   

conn.commit()
conn.close()
