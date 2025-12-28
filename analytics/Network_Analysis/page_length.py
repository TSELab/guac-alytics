import sqlite3
import networkx as nx
from prettytable import PrettyTable
import time
import markdown
import re
from constants import DB_LOC, CONSTRUCT_GRAPH

def get_items():
    conn = sqlite3.connect(DB_LOC)
    cursor = conn.cursor()
    query = CONSTRUCT_GRAPH
    cursor.execute(query)
    items = cursor.fetchall()
    G = nx.DiGraph()
    G.add_edges_from(items)
    # G.remove_edges_from(nx.selfloop_edges(G))
    # Get the out-degree of each node
    out_degrees = [node for node, out_degree in G.out_degree() if out_degree == 0]
    conn.close()

    return out_degrees,G

def calculate_path_lengths(G, nodes, out_degrees):
    results = []
    i=1
    # Iterate over all nodes as the source node
    for source_node in nodes:
        print(i," - ",source_node)
        # Calculate all possible path lengths from the source node to other nodes
        path_lengths = []
        for node in out_degrees:
            try:
                path_lengths.append(nx.shortest_path_length(G, source=source_node, target=node))
            except nx.exception.NetworkXNoPath:
                pass
        
        # If there are any path lengths, add the shortest, longest, and mean path lengths to the results
        if path_lengths:
            shortest_path_length = min(path_lengths)
            longest_path_length = max(path_lengths)
            mean_path_length = sum(path_lengths) / len(path_lengths)
            results.append((source_node, longest_path_length, shortest_path_length, mean_path_length))
        i+=1
    return results

def main():
    t_in = time.time()
    out_degrees,G = get_items()
    # Open the markdown file and read its contents
    with open('plots/graph_out.md', 'r') as f:
        md_text = f.read()

    # Convert the markdown text to HTML
    html_text = markdown.markdown(md_text)

    # Remove HTML tags
    clean_text = re.sub('<[^<]+?>', '', html_text)

    # Split lines on "-" and remove leading/trailing spaces
    lines = [line.strip() for line in clean_text.split('\n') if line.strip() != '']
    lines = [line for line in lines if line != '+-----+---------------------------------------------------------+------------+']

    # Split each line on "|" and remove leading/trailing spaces
    parsed_lines = []
    for line in lines:
        items = [item.strip() for item in line.split('|') if item.strip() != '']
        parsed_lines.append(items)

    nodes=[]
    # Print the parsed lines
    for items in parsed_lines:
        if(items[1]!= '-' and items[1]!='Package Name'):
            nodes.append(items[1])

    results = calculate_path_lengths(G, nodes, out_degrees)
    print(2)
    # Sort the results by longest path length in descending order and take the top 500
    top_nodes = sorted(results, key=lambda x: x[1], reverse=True)[:500]
    # Create a table with the top nodes and their path lengths
    myTable = PrettyTable(["Sno", "Package", "Longest Path Length", "Shortest Path Length", "Mean Path Length"])
    for i, (node, longest_path_length, shortest_path_length, mean_path_length) in enumerate(top_nodes, 1):
        myTable.add_row([i, node, longest_path_length, shortest_path_length, mean_path_length])
    myTable.add_row(['-', '-', '-', '-', '-'])

    # Write the table to a file
    data = myTable.get_string()
    with open('plots/path_length.md', 'w') as f:
        f.write(data)

    t_out = time.time()
    print('Program run time in seconds:', t_out - t_in, '(s)')

if __name__ == '__main__':
    main()



