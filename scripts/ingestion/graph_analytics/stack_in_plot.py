from calendar import month
import datetime
import sqlite3
import time

import matplotlib.pyplot as plt
import networkx as nx

days = [k for k in range(1,70)]

def build_plot(CUR, before):
    monthly_track = monthly(CUR, before)
    stacks = list(monthly_track.values())
    labels = [key for key in monthly_track.keys()]
    plt.stackplot(days, stacks, labels=labels)
    plt.title("Monthly evolution of top-10 packages")
    plt.legend(loc="upper left")
    plt.xlabel("Monthly Increment")
    plt.ylabel("In-degree")
    plt.tight_layout()
    plt.savefig('/data/yellow/vineet/results/plots/evolve_in.png')


def monthly(CUR, before):
    high_packages = top_10(CUR, before)
    mon = [k for k in range(1, 13)]
    com = [(2017, i) for i in mon[1:]]
    com = com + [(2018, i) for i in mon]
    com = com + [(2019, i) for i in mon]
    com = com + [(2020, i) for i in mon]
    com = com + [(2021, i) for i in mon]
    com = com + [(2022, i) for i in mon[:10]]

    monthly_track = {}
    for pack in high_packages.keys():
        monthly_track[pack] = []

    for cm in com:
        after = datetime.datetime(year=cm[0], month=cm[1], day=1) - datetime.timedelta(seconds=1)
        G = nx.DiGraph()
        query = '''
            SELECT s.source_name||'_'||s.version||'_'||bi.type, 
                b.package||'_'||b.version||'_'||b.architecture
            FROM dependency_table d 
            JOIN buildinfo_table bi ON bi.buildinfo_id = d.buildinfo_id
            JOIN source_table s ON s.source_id = bi.source_id
            JOIN binary_table b ON b.binary_id = d.binary_id
            WHERE bi.build_date BETWEEN '{}' AND '{}'
            '''.format(before, after)

        CUR.execute(query)
        items = CUR.fetchall()

        G.add_edges_from(items)

        for pack in monthly_track.keys():
            if pack in G.nodes():
                monthly_track[pack].append(G.in_degree(pack))
            else:
                monthly_track[pack].append(0)
        print(after)
    return monthly_track


def top_10(CUR, before):
    after = datetime.datetime(year=2022, month=10, day=1) - datetime.timedelta(seconds=1)
    query = '''
    SELECT s.source_name||'_'||s.version||'_'||bi.type, 
        b.package||'_'||b.version||'_'||b.architecture
    FROM dependency_table d 
    JOIN buildinfo_table bi ON bi.buildinfo_id = d.buildinfo_id
    JOIN source_table s ON s.source_id = bi.source_id
    JOIN binary_table b ON b.binary_id = d.binary_id
    WHERE bi.build_date BETWEEN '{}' AND '{}'
    '''.format(before, after)

    CUR.execute(query)
    items = CUR.fetchall()

    G = nx.DiGraph()
    G.add_edges_from(items)

    nodes_sorted_by_degree = sorted(G.nodes, key=G.in_degree, reverse=True)
    top_degree_nodes = nodes_sorted_by_degree[:10]

    high_packages = {}

    for i in top_degree_nodes:
        high_packages[i] = G.in_degree(i)

    print('high packages:', high_packages)
    return high_packages


if __name__ == "__main__":
    
    t_in = time.time()
    CONN = sqlite3.connect('/data/yellow/vineet/database/bi_multi_tables.db')
    CUR = CONN.cursor()
    before = datetime.datetime(year=2017, month=1, day=1)
    build_plot(CUR,before)
    CONN.commit()    
    CONN.close()
    t_out = time.time()
    print('Program run time in seconds:', t_out - t_in, '(s)')
