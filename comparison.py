import collections

import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
from scipy.optimize import curve_fit
year = 2015
network = "vldb"

def func(a,x,b):
    return a * pow(x,b)

def compare():
    sns.set()
    for network in ["vldb", "sigmod", "icde", "icdt", "edbt", "pods", "db"]:
        # sns.distplot("./eps/")
        graph = nx.read_gml("../dblp-" + str(year) + "/" + network + ".gml")
        edge_weights_sequence = sorted([graph[edg[0]][edg[1]]["cc"] for edg in graph.edges(data=True)])
        edge_count = collections.Counter(edge_weights_sequence)
        edge_weight, cnt = zip(*edge_count.items())
        with open("../dblp-" + str(year) + "/" + network + "-cc.txt", "w") as file:
            i = 0
            for edgwght in edge_weight:
                file.write(str(edgwght)+"\t"+str(cnt[i])+"\n")
                i += 1
        # plt.semilogx(edge_weight, cnt, marker=".", markersize=15, color="green")
        plt.plot(edge_weight, cnt, 'b-', label='data')
        popt, pcov = curve_fit(func, edge_weight, cnt)
        plt.plot(edge_weight, func(edge_weight, *popt), 'r-',label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
        plt.title(network + "-2015 network  Communication cost Histogram")
        plt.ylabel("Count")
        plt.xlabel("Communication cost")
        plt.show()
        plt.savefig("./eps/" + network + "-cc.png", dpi=1000)


if __name__ == '__main__':
    compare()
