import sqlite3
import networkx as nx
from prettytable import PrettyTable
import cpnet
import time

# Define function to retrieve edge data from SQLite database
def get_edge_data():
    conn = sqlite3.connect('/data/yellow/guacalytics/database/bi_multi_tables.db')
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
    conn.close()
    return items

# Define function to create directed graph and calculate MINRES metric for each node
def get_top_nodes(items):
    G = nx.DiGraph()
    G.add_edges_from(items)

    alg = cpnet.MINRES()
    alg.detect(G)
    pair_id = alg.get_pair_id()
    coreness = alg.get_coreness()

    top_nodes = sorted(coreness.items(), key=lambda x: x[1], reverse=True)[:500]
    return top_nodes

# Define function to insert top node data into a table format in a md file
def insert_into_md(top_nodes):
    myTable = PrettyTable(["Sno","Top 500 coreness value packages", "CP-MINRES"])
    i=0
    for node, value in top_nodes:
        myTable.add_row([i , node , value])
        i+=1
    myTable.add_row([ '-' , '-','-'])

    data = myTable.get_string()
    with open('plots/minres.md', 'w') as f:
            f.write(data)

# Main function to call other functions
def main():
    t_in = time.time()
    print("program running")

    items = get_edge_data()
    top_nodes = get_top_nodes(items)
    insert_into_md(top_nodes)

    t_out = time.time()
    print('Program run time in seconds:', t_out - t_in, '(s)')

if __name__ == '__main__':
    main()
