#!/usr/bin/env python
import sqlite3

LOCATION = '/data/yellow/vineet/database/bi_multi_tables.db'

def init_db(location = LOCATION):
    conn = sqlite3.connect(location)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS source_table (
            source_id INTEGER PRIMARY KEY,
            source_name varchar,
            version varchar,
            location varchar,
            unique(source_name,version))""")  
     
    cur.execute(""" CREATE TABLE IF NOT EXISTS buildinfo_table (
            buildinfo_id INTEGER PRIMARY KEY,
            source_id integer,
            type varchar,
            build_origin varchar,
            build_architecture varchar,
            build_date datetime,
            build_path varchar,
            environment varchar,
            unique(source_id,type,build_date),
            FOREIGN KEY(source_id) references source_table(source_id) )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS binary_table (
            binary_id INTEGER PRIMARY KEY,
            package varchar,
            version varchar,
            architecture varchar)""")  

    cur.execute("""CREATE TABLE IF NOT EXISTS dependency_table (
            buildinfo_id INTEGER,
            binary_id INTEGER,
            FOREIGN KEY(buildinfo_id) references buildinfo_table(buildinfo_id),
            FOREIGN KEY(binary_id) references binary_table(binary_id) )""")  

    cur.execute("""CREATE TABLE IF NOT EXISTS output_table (
            buildinfo_id INTEGER,
            binary_id INTEGER,
            checksum_md5 varchar,
            checksum_sha1 varchar,
            checksum_sha256 varchar,
            unique(buildinfo_id,binary_id,checksum_md5)
            FOREIGN KEY(buildinfo_id) references buildinfo_table(buildinfo_id),
            FOREIGN KEY(binary_id) references binary_table(binary_id) )""")

    conn.commit()
    conn.close()

INSERT_SOURCE = '''INSERT OR IGNORE INTO source_table (source_id,source_name,version) VALUES (null,?,?)'''
INSERT_BUILD = '''INSERT OR IGNORE INTO buildinfo_table (buildinfo_id,source_id,type,build_origin,build_architecture,build_date,build_path,environment) VALUES (null,?,?,?,?,?,?,?)'''
INSERT_BINARY = '''INSERT OR IGNORE INTO binary_table (binary_id,package,version,architecture) VALUES (null,?,?,?)'''
INSERT_DEPENDENCY = '''INSERT OR IGNORE INTO dependency_table (buildinfo_id,binary_id) VALUES (?,?)'''
INSERT_OUTPUT = '''INSERT OR IGNORE INTO output_table (buildinfo_id,binary_id,checksum_md5,checksum_sha1,checksum_sha256) VALUES (?,?,?,?,?)'''

def insert_build(cur, result, build_time, deps,output):
    # Inserting data into source_table

    cur.execute(INSERT_SOURCE, (result['Source'], result['Version']))

    # see https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.lastrowid 
    # (warning, it's nonportable or threadsafe)
    cur.execute('''select source_id from source_table where source_name='{}' and version='{}' '''.format(result['Source'],result['Version']))
    id1 = cur.lastrowid

    # inserting data into buildinfo_table
    cur.execute(INSERT_BUILD,
                (id1,
                 result['Architecture'], result['Build-Origin'], result['Build-Architecture'],
                 build_time, result['Build-Path'], result['Environment']))

    cur.execute('''select buildinfo_id from buildinfo_table where type='{}' and source_id='{}' '''.format(result['Architecture'],id1))
    # build_id=cur.fetchone()[0]
                
    build_id = cur.lastrowid

    # we insert the binaries we just created
    binary_ids = []
    if output:
        for binary,md5,sha1,sha256 in output:
            cur.execute(INSERT_BINARY, (binary, result['Version'], result['Architecture']))
            binary_id = cur.lastrowid
            cur.execute(INSERT_OUTPUT, (build_id, binary_id, str(md5), str(sha1), str(sha256)))
            binary_ids.append(binary_id)


    # we get the ids as we update the binary table with the dependencies
    # inserting dependencies into binary table
    if deps:
        for package, name, version in deps:
            cur.execute(INSERT_BINARY, (name, version, result['Architecture']))
            binary_ids.append(cur.lastrowid)
            
        for binary_id in binary_ids:
            cur.execute(INSERT_DEPENDENCY, (build_id, binary_id))
