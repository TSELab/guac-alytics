import sqlite3
import networkx as nx
import matplotlib.pyplot as plt    
import statistics
import time
import datetime
import numpy as np
import math

def create_plot(days, data, title, xlabel, ylabel, legend_labels=None, save_path=None, figsize=None, annotate=None):
    """
    Create a plot based on the given data and parameters.
    
    Parameters:
    - days: array-like object with the x-axis values
    - data: dictionary with the y-axis data (keys are legend labels, values are arrays of y-axis values)
    - title: string with the plot title
    - xlabel: string with the x-axis label
    - ylabel: string with the y-axis label
    - legend_labels: array-like object with the legend labels (optional)
    - save_path: string with the file path where the plot should be saved (optional)
    - figsize: tuple with the figure size (optional)
    - annotate: dictionary with annotations (keys are days, values are the text to annotate) (optional)
    """
    
    # Create the figure
    plt.figure(figsize=figsize)
    plt.grid(True, which="both")
    
    # Plot each set of data
    for label, values in data.items():
        plt.plot(days, values, label=label, marker='o')
    
    # Annotate the plot if necessary
    if annotate is not None:
        for day, text in annotate.items():
            idx = np.where(days == day)[0][0]
            plt.annotate(text, xy=(days[idx], max(data.values())[idx]), xytext=(days[idx]+0.05, max(data.values())[idx]+0.05), rotation=90, size=10)
    
    # Add legend and axis labels
    if legend_labels is not None:
        plt.legend(legend_labels)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(days)
    
    # Save the plot if necessary
    if save_path is not None:
        plt.savefig(save_path, dpi=1200)
    
    # Show the plot
    plt.show()
    plt.close()


def compute_statistics(degree_sequence,G):
    """
    Computes statistics (mean, median, percentile, standard deviation) for a given degree sequence.

    Parameters:
    degree_sequence (list): list of in-degree values for nodes in a graph
    G : directed dependency graph

    """
    mean_list.append(math.log(statistics.mean(degree_sequence)) if statistics.mean(degree_sequence) != 0 else 0.0)
    median_list.append(math.log(statistics.median(degree_sequence)) if statistics.median(degree_sequence) != 0 else 0.0)
    std_dev_list.append(math.log(np.std(degree_sequence)) if np.std(degree_sequence) != 0 else 0.0)
    max_list.append(max(degree_sequence))
    highest_degree_node.append(max(G.nodes, key=G.in_degree) if len(G.nodes()) != 0 else 0.0)
    perc_25_list.append(math.log(np.percentile(degree_sequence, 25)) if np.percentile(degree_sequence, 25) != 0 else 0.0)
    perc_75_list.append(math.log(np.percentile(degree_sequence, 75)) if np.percentile(degree_sequence, 75) != 0 else 0.0)
    

def build_graph():
    """
    Builds a directed graph for each time interval specified by DATE1 and DATE2 and computes in-degree statistics for the graph.
    """
    for i in range(len(days)):
        query = ''' SELECT s.source_name||'_'||s.version||'_'||bi.type, 
                b.package||'_'||b.version||'_'||b.architecture
            FROM dependency_table d 
            JOIN buildinfo_table bi ON bi.buildinfo_id = d.buildinfo_id
            JOIN source_table s ON s.source_id = bi.source_id
            JOIN binary_table b ON b.binary_id = d.binary_id
            WHERE bi.build_date BETWEEN '{}' AND '{}'
            '''.format(date1[i], date2[i])

        cur.execute(query)
        items = cur.fetchall()
        G = nx.DiGraph()
        G.add_edges_from(items)    
        print(i)

        if len(G.nodes()) == 0:
            degree_sequence = [0]
        else:
            degree_sequence = [G.in_degree(n) for n in G.nodes]
        
        compute_statistics(degree_sequence,G)
 

if __name__ == '__main__':
    t_in = time.time()
    days = [k for k in range(1,24)]

    mean_list = []
    median_list = []
    std_dev_list = []
    highest_degree_node = []
    max_list = []
    perc_25_list = []
    perc_75_list = []

    before = datetime.datetime(year=2017, month=1, day=1)
    after = datetime.datetime(year=2022, month=10, day=1) - datetime.timedelta(seconds=1)
    delta=after-before
    num=int(delta.days/len(days))
    date2 = [before + datetime.timedelta(days=int(num*i)) for i in range(1,len(days)+1)]
    date1=[before + datetime.timedelta(days=int(num*i)) for i in range(len(days))]

    conn = sqlite3.connect('/data/yellow/guacalytics/database/bi_multi_tables.db')
    cur = conn.cursor()

    build_graph()

    # Plot 1
    data = {"25th percentile": perc_25_list, "median": median_list, "75th percentile": perc_75_list, "mean": mean_list, "max. degree value": max_list}
    create_plot(days, data, "In-degree Statistical measures(log) for all source architectures", "quarterly tracking", "Statistical Measures ", annotate=None, save_path='plots/stat_in.png')

    # Plot 2
    data = {"max in-degree": max_list}
    create_plot(days, data, "Max In-degree tracking for all source architectures", "quarterly tracking", "In-degree", legend_labels=["max in-degree"], annotate=dict(zip(days, highest_degree_node)), save_path='plots/max_in.png')

    # Plot 3
    data = {"mean": mean_list}
    annotations = {day: txt for day, txt in zip(days, std_dev_list)}
    create_plot(days, data, "Mean In-degree and Std. deviation for all source architectures", "quarterly tracking", "Mean In-degree(log) and Standard Deviation", legend_labels=["mean", "std. dev"], data_kwargs=dict(yerr=std_dev_list), annotate=annotations, save_path='plots/mean_in.png')

    # Plot 4
    data = {"std. deviation": std_dev_list}
    create_plot(days, data, "Std. deviation (log)", "quarterly tracking", "Standard deviation", annotate=None, save_path='plots/std_in.png')

    conn.close()
    t_out = time.time()
    print('Program run time in seconds:', t_out - t_in, '(s)')
