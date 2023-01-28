import sqlite3
import networkx as nx
import time
import datetime
from prettytable import PrettyTable

t_in = time.time()

CONN = sqlite3.connect('/data/yellow/vineet/database/bi_multi_tables.db')
CUR = CONN.cursor()

BEFORE = datetime.datetime(year=2017, month=1, day=1)
# BEFORE = datetime.datetime(year=2020, month=1, day=1)
AFTER = datetime.datetime(year=2022, month=10, day=1) - datetime.timedelta(seconds=1)
QUERY = '''SELECT source,deps from buildinfo_data WHERE time BETWEEN '{}' AND '{}' '''.format( BEFORE, AFTER)
CUR.execute(QUERY)
G=nx.DiGraph()

myTable = PrettyTable(["Period","Package Name", "In-Degree"])
items = CUR.fetchall()

for item in items:
    N = []
    temp = str(item[1])
    temp = temp[1:len(temp)-1]
    temp = temp.replace("'","")
    jarray = temp.split(",")
    for i in range (len(jarray)):
        cell = (item[0],jarray[i])
        N.append(cell)

    G.add_edges_from(N)
        
nodes_sorted_by_degree = sorted(G.nodes, key=G.in_degree, reverse=True)
top_degree_nodes = nodes_sorted_by_degree[:10]
high_packages = {}

for i in top_degree_nodes:
    high_packages[i] = G.in_degree(i)

degree_value = [G.in_degree(n) for n in high_packages]

for i in range(10):
    myTable.add_row([str(BEFORE) + '  -  ' + str(AFTER) , top_degree_nodes[i], degree_value[i]])

myTable.add_row(['-', '-' , '-'])
data = myTable.get_string()
with open('/data/yellow/vineet/results/plots/in_deg(17-22).md', 'w') as f:
        f.write(data)

CONN.commit()
CONN.close()
t_out = time.time()
print('Program run time in seconds:', t_out - t_in, '(s)')
