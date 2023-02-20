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

days = [k for k in range(1,24)]

mean_list = []
median_list = []
std_dev_list = []
# min_list = []
highest_degree_node = []
max_list = []
perc_25_list = []
perc_75_list = []

#mean plots
def plot_statisctics():
# plot1
    plt.figure()
    plt.grid(True, which ="both")
    print(median_list)
    print(perc_25_list)
    # plt.plot(days, min_list, label = "min. degree value", marker = 'o')
    plt.plot(days, perc_25_list, label = "25th percentile", marker = 'o')
    plt.plot(days, median_list, label = "median", marker = 'o')
    plt.plot(days, perc_75_list, label = "75th percentile", marker = 'o')
    plt.plot(days, mean_list, label = "mean", marker = 'o')
    plt.plot(days, max_list, label = "max. degree value", marker = 'o')
    plt.legend()
    plt.xlabel('quarterly tracking')
    plt.ylabel('values')
    plt.title('Out-degree Statistical measures(log) for all source architectures')
    plt.xticks(days)
    plt.tight_layout()
    plt.savefig('/data/yellow/vineet/results/plots/stat_out.png')
    plt.close()

#plot2
    plt.figure(figsize=(10,10))
    plt.grid(True, which ="both")
    plt.plot(days, max_list, label = "max. degree", marker = 'o')
    for i, txt in enumerate(highest_degree_node):
        plt.annotate(txt, (days[i], max_list[i]), rotation=90, size = 10)

    plt.xlabel('quarterly tracking')
    plt.ylabel('Out-degree')
    plt.title('Max out-degree tracking for all source architectures')
    plt.xticks(days)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('/data/yellow/vineet/results/plots/max_out.png')
    plt.close()

#plot3
    plt.figure()
    plt.grid(True, which ="both")
    plt.plot(days, mean_list, label='mean', marker = 'o')
    plt.fill_between(days, mean_list, [(i+j) for i,j in zip(mean_list, std_dev_list)], interpolate=True, color = 'yellow', alpha=0.25)
    plt.fill_between(days, mean_list, [(i-j) for i,j in zip(mean_list, std_dev_list)], interpolate=True, color = 'yellow', alpha=0.25, label='std. dev')
    plt.legend()
    plt.xlabel('quarterly tracking')
    plt.ylabel('Mean out-degree(log)')
    plt.title('Mean out-degree and Std. deviation for all source architectures')
    plt.xticks(days)
    plt.tight_layout()
    plt.savefig('/data/yellow/vineet/results/plots/mean_out.png')
    plt.close()

# plot4
    plt.figure()
    plt.grid(True, which ="both")
    plt.plot(days, std_dev_list, label = "std. deviation", marker = 'o')
    plt.legend(loc="upper left")
    plt.legend(bbox_to_anchor=(0.5,-0.25))
    plt.legend()
    plt.xlabel('quaterly tracking')
    plt.ylabel('Std. deviation')
    plt.title('Std. deviation (log)')
    plt.xticks(days)
    plt.savefig('/data/yellow/vineet/results/plots/std_out.png',dpi=1200)
    plt.close()


def compute_statisctics(degree_sequence):
    mean_list.append(math.log(statistics.mean(degree_sequence)) if statistics.mean(degree_sequence) != 0 else 0.0)
    median_list.append(math.log(statistics.median(degree_sequence)) if statistics.median(degree_sequence) != 0 else 0.0)
    std_dev_list.append(math.log(np.std(degree_sequence)) if np.std(degree_sequence) != 0 else 0.0)
    # min_list.append(math.log(min(degree_sequence)) if min(degree_sequence) != 0 else 0.0)
    max_list.append(max(degree_sequence))
    highest_degree_node.append(max(G.nodes, key=G.out_degree) if len(G.nodes()) != 0 else 0.0)
    perc_25_list.append(math.log(np.percentile(degree_sequence, 25)) if np.percentile(degree_sequence, 25) != 0 else 0.0)
    perc_75_list.append(math.log(np.percentile(degree_sequence, 75)) if np.percentile(degree_sequence, 75) != 0 else 0.0)
    

def build_graph():
    for i in range(len(days)):
        query = ''' SELECT s.source_name||'_'||s.version||'_'||bi.type, 
                b.package||'_'||b.version||'_'||b.architecture
            FROM dependency_table d 
            JOIN buildinfo_table bi ON bi.buildinfo_id = d.buildinfo_id
            JOIN source_table s ON s.source_id = bi.source_id
            JOIN binary_table b ON b.binary_id = d.binary_id
            WHERE bi.build_date BETWEEN '{}' AND '{}'
            '''.format(DATE1[i], DATE2[i])

        CUR.execute(query)
        items = CUR.fetchall()

        G.add_edges_from(items)    
        print(i)

        if len(G.nodes()) == 0:
            degree_sequence = [0]
        else:
            degree_sequence = [G.out_degree(n) for n in G.nodes]
        
        compute_statisctics(degree_sequence)
    
    plot_statisctics()
 
    
CONN = sqlite3.connect('/data/yellow/vineet/database/bi_multi_tables.db')
CUR = CONN.cursor()

BEFORE = datetime.datetime(year=2017, month=1, day=1)
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
