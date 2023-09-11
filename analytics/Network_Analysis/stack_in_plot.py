from calendar import month
import datetime
import sqlite3
import time
import matplotlib.pyplot as plt
import networkx as nx
from constants import DB_LOC, GRAPH_DATES

days = [k for k in range(1,70)]

def build_plot(CUR, before):
    #  Get monthly data for top 10 packages
    monthly_track = monthly(CUR, before)
    stacks = list(monthly_track.values())
    labels = [key for key in monthly_track.keys()]
    # Plot the data
    plt.stackplot(days, stacks, labels=labels)
    plt.title("Monthly evolution of top-10 packages")
    plt.legend(loc="upper left")
    plt.xlabel("Monthly Increment")
    plt.ylabel("In-degree")
    plt.tight_layout()
    plt.savefig('plots/evolve_in.png')


def monthly(CUR, before):
    # Get the top 10 packages from the last month
    high_packages = top_10(CUR, before)
    com = [(year, month) for year in range(2017, 2023) for month in range(1, 13)]
    com = com[:-4] + [(2022, month) for month in range(1, 11)]

    monthly_track = {}
    for pack in high_packages.keys():
        monthly_track[pack] = []
    
    # Loop through each month and calculate the in-degree of each package
    for cm in com:
        # Calculate the date range for the current month
        after = datetime.datetime(year=cm[0], month=cm[1], day=1) - datetime.timedelta(seconds=1)
        G = nx.DiGraph()
        query = GRAPH_DATES.format(before, after)

        CUR.execute(query)
        items = CUR.fetchall()

        G.add_edges_from(items)
         # Calculate the in-degree of each package and add it to the monthly data
        for pack in monthly_track.keys():
            if pack in G.nodes():
                monthly_track[pack].append(G.in_degree(pack))
            else:
                monthly_track[pack].append(0)
        print(after)
    return monthly_track


def top_10(CUR, before):
    # Calculate the date range for the month
    after = datetime.datetime(year=2022, month=10, day=1) - datetime.timedelta(seconds=1)
    query = GRAPH_DATES.format(before, after)

    CUR.execute(query)
    items = CUR.fetchall()

    G = nx.DiGraph()
    G.add_edges_from(items)

    # Find the top 10 packages by in-degree
    nodes_sorted_by_degree = sorted(G.nodes, key=G.in_degree, reverse=True)
    top_degree_nodes = nodes_sorted_by_degree[:10]

    high_packages = {}
    # Add the top 10 packages and their in-degree to a dictionary
    for i in top_degree_nodes:
        high_packages[i] = G.in_degree(i)

    print('high packages:', high_packages)
    return high_packages


if __name__ == "__main__":
    
    t_in = time.time()
    CONN = sqlite3.connect(DB_LOC)
    CUR = CONN.cursor()
    before = datetime.datetime(year=2017, month=1, day=1)
    build_plot(CUR,before)
    CONN.commit()    
    CONN.close()
    t_out = time.time()
    print('Program run time in seconds:', t_out - t_in, '(s)')
