import sqlite3
import networkx as nx
import time
from prettytable import PrettyTable

t_in = time.time()
   
def top():

    query = '''SELECT source_table.source_name, source_table.version, buildinfo_table.type,
                  binary_table.package, binary_table.version, binary_table.architecture
           FROM dependency_table
           JOIN buildinfo_table ON dependency_table.buildinfo_id = buildinfo_table.buildinfo_id
           JOIN source_table ON buildinfo_table.source_id = source_table.source_id
           JOIN binary_table ON dependency_table.binary_id = binary_table.binary_id'''
    CUR.execute(query)
    items=CUR.fetchall()
    for item in items:
        i = '_'.join(item[:3])
        j = '_'.join(item[3:])
        G.add_edge(i, j)
    
# Calculating in-degree and sorting the packages to get the top ones  
    nodes_sorted_by_degree = sorted(G.nodes, key=G.in_degree, reverse=True)
	
    top_degree_nodes = nodes_sorted_by_degree
    myTable = PrettyTable(["Sno","Package Name", "In-Degree"])
    degree_value = [G.in_degree(n) for n in top_degree_nodes]
    for i in range(500):
        myTable.add_row([i,top_degree_nodes[i], degree_value[i]])

    myTable.add_row(['-','-' , '-'])

    data = myTable.get_string()

    with open('/data/yellow/vineet/results/plots/graph_in.md', 'w') as f:
        f.write(data)
     
# Calculating out-degree and sorting the packages to get the top ones  
    nodes_sorted_by_degree = sorted(G.nodes, key=G.out_degree, reverse=True)
	
    top_degree_nodes = nodes_sorted_by_degree
    myTable = PrettyTable(["Sno","Package Name", "Out-Degree"])
    degree_value = [G.out_degree(n) for n in top_degree_nodes]
    for i in range(500):
        myTable.add_row([i,top_degree_nodes[i], degree_value[i]])

    myTable.add_row(['-','-' , '-'])

    data = myTable.get_string()

    with open('/data/yellow/vineet/results/plots/graph_out.md', 'w') as f:
        f.write(data)
        
CONN = sqlite3.connect('/data/yellow/vineet/database/bi_multi_tables.db')
CUR = CONN.cursor()
G = nx.DiGraph()
top()
    
CONN.commit()    
CONN.close()
t_out = time.time()
print('Program run time in seconds:', t_out - t_in, '(s)')
