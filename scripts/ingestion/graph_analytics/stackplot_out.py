from calendar import month
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt      #Plot
import time
import datetime

t_in = time.time()

def build_plot():
    monthly_track = monthly()
    stacks = list(monthly_track.values())
    labels = [key for key in monthly_track.keys()]
    plt.stackplot(days, stacks, labels=labels)
    plt.title("monthly evolution(2017-2022(Sep))")
    plt.legend()
    plt.xlabel("monthly increment")
    plt.ylabel("Out-degree")
    plt.tight_layout()
    plt.savefig('/data/yellow/vineet/results/plots/evolve_out(17-22).png')

def monthly():
    high_packages = top_10()
    mon = [k for k in range (1,13)]
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
        G=nx.DiGraph()
        QUERY = '''SELECT source,deps from buildinfo_data WHERE arch = '{}' and time BETWEEN '{}' AND '{}' '''.format(ARCH,before,after)
        CUR.execute(QUERY)
        items = CUR.fetchall()
        for item in items:
            N = []
            temp = str(item[1])
            temp = temp[1:len(temp)-1]
            temp = temp.replace("'","")
            jarray = temp.split(",")
            for i in range (len(jarray)):
                cell = (item[0],jarray[i])
                N.append(cell)

            G.add_edges_from(N)

        for pack in monthly_track.keys():
            if pack in G.nodes():
                monthly_track[pack].append(G.out_degree(pack))
            else:
                monthly_track[pack].append(0)
        print(after)
    return monthly_track
   
def top_10():
    after = datetime.datetime(year=2022, month=10, day=1) - datetime.timedelta(seconds=1)
    QUERY = '''SELECT source,deps from buildinfo_data WHERE arch = '{}' and time BETWEEN '{}' AND '{}' '''.format(ARCH,before,after)
    CUR.execute(QUERY)
    items = CUR.fetchall()

    for item in items:
        N = []
        temp = str(item[1])
        temp = temp[1:len(temp)-1]
        temp = temp.replace("'","")
        jarray = temp.split(",")
        for i in range (len(jarray)):
            cell = (item[0],jarray[i])
            N.append(cell)

        G.add_edges_from(N)

    nodes_sorted_by_degree = sorted(G.nodes, key=G.out_degree, reverse=True)
    top_degree_nodes = nodes_sorted_by_degree[:10]

    high_packages = {}

    for i in top_degree_nodes:
        high_packages[i] = G.out_degree(i)

    print('high packages:', high_packages)
    return high_packages

CONN = sqlite3.connect('/data/yellow/vineet/database/bi_multi_tables.db')
CUR = CONN.cursor()
before = datetime.datetime(year=2017, month=1, day=1)
G = nx.DiGraph()
ARCH = 'amd64'
# days = [k for k in range(1,34)]
days = [k for k in range(1,70)]

build_plot()
    
CONN.commit()    
CONN.close()
t_out = time.time()
print('Program run time in seconds:', t_out - t_in, '(s)')
