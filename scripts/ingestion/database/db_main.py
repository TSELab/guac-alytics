import sqlite3
from ..constants import DB_LOC

LOCATION = DB_LOC

def open_db(location = LOCATION):
    conn = sqlite3.connect(location)
    return conn

def close_db(conn = None):
    if not conn:
        raise Exception("I need a database handle to close!")
    conn.close()