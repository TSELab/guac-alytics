#!/usr/bin/env python
import sqlite3

def target_con(con):
        conn = sqlite3.connect(con)
        cur = conn.cursor()
        return cur

target_con('/data/yellow/vineet/database/bi_multi_tables.db')
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
