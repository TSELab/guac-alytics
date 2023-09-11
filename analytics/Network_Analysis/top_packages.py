import sqlite3
import networkx as nx
import time
from prettytable import PrettyTable
from constants import DB_LOC, CONSTRUCT_GRAPH

def get_top_packages():
    """
    Extracts data from the database and calculates in-degree and out-degree for packages, 
    then sorts them to get the top ones. Returns two lists of top packages and their degrees.
    """
    G = nx.DiGraph()
    query = CONSTRUCT_GRAPH
    CUR.execute(query)
    items = CUR.fetchall()

    G.add_edges_from(items)

    # Get the top packages based on in-degree and out-degree and their corresponding degree values
    nodes_sorted_by_in_degree = sorted(G.nodes, key=G.in_degree, reverse=True)
    top_in_degree_nodes = nodes_sorted_by_in_degree[:500]
    in_degree_values = [G.in_degree(n) for n in top_in_degree_nodes]

    nodes_sorted_by_out_degree = sorted(G.nodes, key=G.out_degree, reverse=True)
    top_out_degree_nodes = nodes_sorted_by_out_degree[:500]
    out_degree_values = [G.out_degree(n) for n in top_out_degree_nodes]

    return (top_in_degree_nodes, in_degree_values, top_out_degree_nodes, out_degree_values)


def write_to_file(table_data, file_name):
    """
    Writes the data in a pretty table to a markdown file.
    """
    myTable = PrettyTable(table_data[0])
    for i in range(len(table_data[1])):
        myTable.add_row([i+1, table_data[1][i], table_data[2][i]])
    myTable.add_row(['-', '-' , '-'])

    data = myTable.get_string()

    with open(file_name, 'w') as f:
        f.write(data)


if __name__ == "__main__":
    t_in = time.time()
    CONN = sqlite3.connect(DB_LOC)
    CUR = CONN.cursor()

    # Get the top packages based on in-degree and out-degree
    top_in_degree_nodes, in_degree_values, top_out_degree_nodes, out_degree_values = get_top_packages()

    # Write the top packages based on in-degree to a file
    table_data = (["Sno", "Package Name", "In-Degree"], top_in_degree_nodes, in_degree_values)
    write_to_file(table_data, 'plots/graph_in.md')

    # Write the top packages based on out-degree to a file
    table_data = (["Sno", "Package Name", "Out-Degree"], top_out_degree_nodes, out_degree_values)
    write_to_file(table_data, 'plots/graph_out.md')

    CONN.commit()    
    CONN.close()
    t_out = time.time()
    print('Program run time in seconds:', t_out - t_in, '(s)')
