import sqlite3
import networkx as nx
from prettytable import PrettyTable
import time
from constants import DB_LOC, CONSTRUCT_GRAPH

# Define function to retrieve edge data from SQLite database
def get_edge_data():
    conn = sqlite3.connect(DB_LOC)
    cursor = conn.cursor()
    query = CONSTRUCT_GRAPH
    cursor.execute(query)
    items = cursor.fetchall()
    conn.close()
    return items

# Define function to insert top node data into a table format in a md file
def insert_into_md(top_nodes):
    myTable = PrettyTable(["Sno","Top 5000 valued packages", "Coreness"])
    i=1
    for node, value in top_nodes:
        myTable.add_row([i , node , value])
        i+=1
    myTable.add_row([ '-' , '-','-'])


    data = myTable.get_string()
    with open('plots/coreness.md', 'w') as f:
            f.write(data)

# Define function to create directed graph and calculate Coreness metric for each node
def get_top_nodes(items):
    G = nx.DiGraph()
    G.add_edges_from(items)
    # compute the core number of each node
    G.remove_edges_from(nx.selfloop_edges(G))
    core= nx.core_number(G)
        
    top_nodes = sorted(core.items(), key=lambda x: x[1], reverse=True)[:50000]
    return top_nodes

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
