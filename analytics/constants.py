#!/usr/bin/env python
# encoding: utf-8

DB_LOC = '/data/yellow/vineet/database/bi_multi_tables.db'
CONSTRUCT_GRAPH = ''' SELECT s.source_name||'_'||s.version||'_'||bi.type, 
            b.package||'_'||b.version||'_'||b.architecture
        FROM dependency_table d 
        JOIN buildinfo_table bi ON bi.buildinfo_id = d.buildinfo_id
        JOIN source_table s ON s.source_id = bi.source_id
        JOIN binary_table b ON b.binary_id = d.binary_id'''

GRAPH_DATES = ''' SELECT s.source_name||'_'||s.version||'_'||bi.type, 
        b.package||'_'||b.version||'_'||b.architecture
    FROM dependency_table d 
    JOIN buildinfo_table bi ON bi.buildinfo_id = d.buildinfo_id
    JOIN source_table s ON s.source_id = bi.source_id
    JOIN binary_table b ON b.binary_id = d.binary_id
    WHERE bi.build_date BETWEEN '{}' AND '{}' 
    '''