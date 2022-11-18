#!/usr/bin/env python
import sqlite3

def target_con(con):
       conn = sqlite3.connect(con)
       cur = conn.cursor()
       return cur

target_con('/data/yellow/vineet/database/bi_multi_tables.db')
# Creating table 
cur.execute("""CREATE TABLE IF NOT EXISTS buildinfo_data (
       source varchar,
       version varchar,
       arch varchar,
       time datetime,
       deps varchar)""")   

conn.commit()
conn.close()
