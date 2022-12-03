#!/usr/bin/env python
import sqlite3
import constants as c

def target_con(con):
       conn = sqlite3.connect(con)
       cur = conn.cursor()
       return cur

target_con(c.db_loc)
# Creating table 
cur.execute("""CREATE TABLE IF NOT EXISTS buildinfo_data (
       source varchar,
       version varchar,
       arch varchar,
       time datetime,
       deps varchar)""")   

conn.commit()
conn.close()
