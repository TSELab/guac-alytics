import sqlite3
import networkx as nx
import sqlite3
import matplotlib.pyplot as plt      #Plot
import statistics
import time
import datetime
import numpy as np
import math

t_in = time.time()
print ('program running...')

days = [k for k in range(1,24)]
# days = [k for k in range(1,12)]

mean_list = []
median_list = []
std_dev_list = []
min_list = []
max_list = []
perc_25_list = []
perc_75_list = []
highest_degree_node = []

def plot_statistics():
    plt.figure()
    plt.grid(True, which ="both")
    plt.plot(days, min_list, label = "min. degree value", marker = 'o')
    plt.plot(days, perc_25_list, label = "25th percentile", marker = 'o')
    plt.plot(days, median_list, label = "median", marker = 'o')
    plt.plot(days, perc_75_list, label = "75th percentile", marker = 'o')
    plt.plot(days, mean_list, label = "mean", marker = 'o')
    plt.plot(days, max_list, label = "max. degree value", marker = 'o')
    plt.legend(loc="upper left")
    plt.legend(bbox_to_anchor=(0.5,-0.25))
    plt.legend()
    plt.xlabel('quaterly tracking (2017-2022)')
    plt.ylabel('values')
    plt.title('Statistical measures(log) for amd64 architecture')
    plt.xticks(days)
    plt.savefig('/data/yellow/vineet/results/plots/stat_amd64_in(17-22).png',dpi=1200)
    plt.close()

    plt.figure()
    plt.grid(True, which ="both")
    plt.plot(days, std_dev_list, label = "std. deviation", marker = 'o')
    plt.legend(loc="upper left")
    plt.legend(bbox_to_anchor=(0.5,-0.25))
    plt.legend()
    plt.xlabel('quaterly tracking (2017-2022)')
    plt.ylabel('Std. deviation')
    plt.title('Std. deviation (log) for amd64 architecture')
    plt.xticks(days)
    plt.savefig('/data/yellow/vineet/results/plots/std_amd64_in(17-22).png',dpi=1200)
    plt.close()

    plt.figure()
    plt.grid(True, which ="both")
    plt.plot(days, max_list, label = "max. in-degree", marker = 'o')
    for i, txt in enumerate(highest_degree_node):
        plt.annotate(txt, (days[i], max_list[i]), rotation=90, size = 10)

    plt.xlabel('Quarterly tracking (2017-2022(Sep))')
    plt.ylabel('In-degree')
    plt.title('Max in-degree tracking for amd64 architecture')
    plt.xticks(days)
    plt.legend(loc='best')
    plt.savefig('/data/yellow/vineet/results/plots/max_amd64_in(17-22).png')
    plt.close()

    plt.figure()
    plt.grid(True, which ="both")
    plt.plot(days, mean_list, label='mean', marker = 'o')
    plt.fill_between(days, mean_list, [(i+j) for i,j in zip(mean_list, std_dev_list)], interpolate=True, color = 'yellow', alpha=0.25)
    plt.fill_between(days, mean_list, [(i-j) for i,j in zip(mean_list, std_dev_list)], interpolate=True, color = 'yellow', alpha=0.25, label='std. dev')
    plt.legend()
    plt.xlabel('quarterly tracking (2017-2022(Sep))')
    plt.ylabel('Mean in-degree(log)')
    plt.title('Mean in-degree and Std. deviation for amd64 architectures')
    plt.xticks(days)
    plt.tight_layout()
    plt.savefig('/data/yellow/vineet/results/plots/mean_amd64_in(17-22).png')
    plt.close()

def compute_statistics(degree_sequence):
    mean_list.append(math.log(statistics.mean(degree_sequence)))
    median_list.append(math.log(statistics.median(degree_sequence)))
    std_dev_list.append(math.log(statistics.stdev(degree_sequence)))
    min_list.append(math.log(min(degree_sequence)) if min(degree_sequence) != 0 else 0.0)
    max_list.append(math.log(max(degree_sequence)) if max(degree_sequence) != 0 else 0.0)
    perc_25_list.append(math.log(np.percentile(degree_sequence, 25)) if np.percentile(degree_sequence, 25) != 0 else 0.0)
    perc_75_list.append(math.log(np.percentile(degree_sequence, 75)) if np.percentile(degree_sequence, 75) != 0 else 0.0)
    highest_degree_node.append(max(G.nodes, key=G.in_degree) if len(G.nodes()) != 0 else 0.0)

def build_graph():
    k=0
    for i in range(len(days)):
        degree_sequence=[]
        QUERY = '''SELECT source,deps from buildinfo_data WHERE arch='amd64' AND time BETWEEN '{}' AND '{}' '''.format(DATE1[i], DATE2[i])
        CUR.execute(QUERY)
        items = CUR.fetchall()
        k+=1
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
        print(k)

        if len(G.nodes()) == 0:
            degree_sequence = [0]
            d=[0]
        else:
            degree_sequence = [G.in_degree(n) for n in G.nodes]
            d=[G.in_degree(n) for n in G.nodes]
  
        compute_statistics(degree_sequence)
    plot_statistics()



CONN = sqlite3.connect('/data/yellow/vineet/database/bi_multi_tables.db')
CUR = CONN.cursor()

BEFORE = datetime.datetime(year=2017, month=1, day=1)
# BEFORE = datetime.datetime(year=2020, month=1, day=1)
AFTER = datetime.datetime(year=2022, month=10, day=1) - datetime.timedelta(seconds=1)
DELTA=AFTER-BEFORE
NUM=int(DELTA.days/len(days))
DATE2 = [BEFORE + datetime.timedelta(days=int(NUM*i)) for i in range(1,len(days)+1)]
DATE1=[BEFORE + datetime.timedelta(days=int(NUM*i)) for i in range(len(days))]
G = nx.DiGraph()

build_graph()

CONN.close()
t_out = time.time()
print('Program run time in seconds:', t_out - t_in, '(s)')
