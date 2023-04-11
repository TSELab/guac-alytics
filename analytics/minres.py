import sqlite3
import networkx as nx
import cpnet
import time
import matplotlib.pyplot as plt

def get_edge_data(database_path):
    """
    Retrieve the edge data from the database.

    Args:
    cursor (sqlite3.Cursor): cursor object that allows interaction with the database

    Returns:
    list of tuples: each tuple contains the source and target nodes of an edge
    """
    conn = sqlite3.connect(database_path)
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

def run_minres(items, num_iterations):
    """
    Run the MINRES algorithm on the graph for different numbers of nodes and record the execution times.

    Args:
    items (list of tuples): each tuple contains the source and target nodes of an edge
    num_iterations (int): number of iterations to run the algorithm for

    Returns:
    tuple of lists: the first list contains the number of nodes for each iteration, 
    the second list contains the execution times for each iteration
    """
    t = []
    n = []
    for i in range(1, num_iterations + 1):
        t_in = time.time()
        print(i)
        G = nx.DiGraph()
        for item in items[:30564212 * i]:
            G.add_edge(item[0], item[1])

        alg = cpnet.MINRES()
        alg.detect(G)
        pair_id = alg.get_pair_id()
        coreness = alg.get_coreness()
        t_out = time.time()
        t.append(t_out - t_in)
        n.append(30564212 * i)
    return (n, t)

def plot_results(n, t):
    """
    Plot the execution times against the number of nodes and save the plot to a file.

    Args:
    n (list): the number of nodes for each iteration
    t (list): the execution times for each iteration
    """
    fig, ax = plt.subplots()
    ax.grid(True,which="both")
    ax.plot(n, t)

    # Add labels to the x-axis and y-axis
    ax.set_xlabel('Number of nodes')
    ax.set_ylabel('Time taken for execution')
    ax.set_title("Execution Time vs Number of Nodes for MINRES")
    plt.subplots_adjust(bottom=0.15)
    plt.xticks(n,rotation=45, ha='right')
    plt.savefig('plots/minres.png',dpi=1200)
    plt.close()

# Main program
if __name__ == '__main__':
    t1 = time.time()
    items = get_edge_data('/data/yellow/guacalytics/database/bi_multi_tables.db')
    results = run_minres(items, 20)
    plot_results(results[0], results[1])
    t2 = time.time()
    print('Program run time in seconds:', t2 - t1, '(s)')
