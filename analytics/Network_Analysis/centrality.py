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
def insert_into_md(values):
    with open('plots/centrality.md', 'w') as f:
        f.write('| Package | Coreness | Degree Centrality | Eigenvector Centrality | Betweenness Centrality | Closeness Centrality | Page Rank |\n')
        f.write('| --- | --- | --- | --- | --- | --- | --- |\n')
        for value in values:
            f.write(f'| {value[0]} | {value[1]} | {value[2]} | {value[3]} | {value[4]} | {value[5]} | {value[6]} |\n')
  

# Define function to create directed graph and calculate Eigenvector Centrality metric for each node
def get_top_nodes(items):
    G = nx.DiGraph()
    G.add_edges_from(items)
    # calculate degree centrality
    degree_centrality = nx.degree_centrality(G)

    # calculate eigenvector centrality
    eigenvector_centrality = nx.eigenvector_centrality(G)

    # calculate PageRank
    pagerank = nx.pagerank(G)

    # calculate betweenness centrality
    betweenness_centrality = nx.betweenness_centrality(G,k=500)

    # calculate closeness centrality
    closeness_centrality = nx.closeness_centrality(G)

    G.remove_edges_from(nx.selfloop_edges(G))
    # calculate coreness
    coreness = nx.core_number(G)

    # create a list of tuples with the node, coreness, degree centrality, eigenvector centrality, betweenness centrality, closeness centrality and PageRank values
    values = [(node, coreness[node], degree_centrality[node], eigenvector_centrality[node] , betweenness_centrality[node], closeness_centrality[node], pagerank[node]) for node in G.nodes()]

    # sort the list by coreness
    values.sort(key=lambda x: x[1], reverse=True)
    return values

# Main function to call other functions
def main():
    t_in = time.time()
    print("program running")

    items = get_edge_data()
    values = get_top_nodes(items)
    insert_into_md(values)

    t_out = time.time()
    print('Program run time in seconds:', t_out - t_in, '(s)')

if __name__ == '__main__':
    main()
