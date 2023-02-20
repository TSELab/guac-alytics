import sqlite3
import networkx as nx
from prettytable import PrettyTable
import cpnet
import time


# Connect to the SQLite database and retrieve the edge data
t_in = time.time()
print("program running")
conn = sqlite3.connect('/data/yellow/vineet/database/bi_multi_tables.db')
cursor = conn.cursor()
query = '''
    SELECT s.source_name||'_'||s.version||'_'||bi.type, 
        b.package||'_'||b.version||'_'||b.architecture
    FROM dependency_table d 
    JOIN buildinfo_table bi ON bi.buildinfo_id = d.buildinfo_id
    JOIN source_table s ON s.source_id = bi.source_id
    JOIN binary_table b ON b.binary_id = d.binary_id'''

cursor.execute(query)
items = cursor.fetchall()

G = nx.DiGraph()
G.add_edges_from(items)

# Calculating MINRES metric for each node
alg = cpnet.MINRES()
alg.detect(G)
pair_id = alg.get_pair_id()
coreness = alg.get_coreness()

# Get the 10 nodes with the highest coreness Rossa
top_nodes = sorted(coreness.items(), key=lambda x: x[1], reverse=True)[:500]

myTable = PrettyTable(["Sno","Top 500 coreness value packages", "CP-MINRES"])
i=0
for node, value in top_nodes:
    myTable.add_row([i , node , value])
    i+=1
myTable.add_row([ '-' , '-','-'])


data = myTable.get_string()
with open('/data/yellow/vineet/results/plots/minres.md', 'w') as f:
        f.write(data)

conn.close()
t_out = time.time()
print('Program run time in seconds:', t_out - t_in, '(s)')
