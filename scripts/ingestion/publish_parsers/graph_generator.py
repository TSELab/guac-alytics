# Description: Optional file to generate graph.html file to view the graph

import networkx as nx
from pyvis.network import Network
from .headerparser import parser

def CreateDependency_edges(filename, G):
    with open(filename,'r') as rf:
        header = ""
        for line in rf:
            if line == "\n":
                parsed_package =  parser.parse_string(header).normalized_dict()
                for dependency_list in parsed_package["depends"]:
                    for dependency in dependency_list:
                        if '(' in dependency:
                            dependency_package_name = dependency.split('(')[0]
                        else:
                            dependency_package_name = dependency
                        G.add_edge(parsed_package["package"], dependency_package_name)
                header = ""
            else:
                header += line
    return G

def generate_graph(date, ARCH):
    G = nx.Graph()
    g = Network()

    if date == "sample" or ARCH == "sample":
        G = CreateDependency_edges('Packagelist_DUMP/test', G)
    else:
        for DFSG in ["main", "contrib", "non-free"]:
            CreateDependency_edges(f'Packagelist_DUMP/{date}-{ARCH}-{DFSG}_Packages', G)
    print("Graph created: open graph.html to view graph")
    g.from_nx(G)
    g.show("graph.html")