# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import matplotlib.pyplot as plt

# import make_data_file
from Team import Team
from dblp_ds import DBLP_Data
import Algorithms

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def show_graph(d_graph):
    import networkx as nx
    plt.clf()
    pos = nx.spring_layout(d_graph)  # pos = nx.nx_agraph.graphviz_layout(G)
    nx.draw_networkx(d_graph, pos)
    labels = nx.get_edge_attributes(d_graph, 'weight')
    nx.draw_networkx_edge_labels(d_graph, pos, edge_labels=labels)
    plt.show()


def toy():
    t1 = Team()
    task = ["s1", "s2", "s3", "s4"]
    t1.experts = {"v1", "v2", "v3", "v4"}
    t1.skills = {"v1": ["s1", "s2", "s3", "s4"], "v2": ["s1", "s2", "s3"], "v3": ["s1", "s2"], "v4": ["s1"]}
    t2 = Team()
    t2.experts = {"v5", "v6", "v7", "v8"}
    t2.skills = {"v5": ["s1", "s2", "s3"], "v6": ["s1", "s2", "s4"], "v7": ["s1", "s3", "s4"],
                 "v8": ["s2", "s3", "s4"]}
    t3 = Team()
    t3.experts = {"v9", "v10", "v11", "v12"}
    t3.skills = {"v9": ["s1", "s4"], "v10": ["s2", "s3"], "v11": ["s1", "s3"], "v12": ["s2", "s4"]}
    t4 = Team()
    t4.experts = {"v13", "v14", "v15", "v16"}
    t4.skills = {"v13": ["s1"], "v14": ["s2"], "v15": ["s3"], "v16": ["s4"]}
    import networkx as nx
    graph1 = nx.Graph()
    graph2 = nx.Graph()
    graph3 = nx.Graph()
    graph4 = nx.Graph()
    graph1.add_nodes_from([("v1", {"skills": "s1,s2,s3,s4"}), ("v2", {"skills": "s1,s2,s3"}),
                           ("v3", {"skills": "s1,s2"}), ("v4", {"skills": "s1"})])
    graph2.add_nodes_from([("v5", {"skills": "s1,s2,s3"}), ("v6", {"skills": "s1,s2,s4"}),
                           ("v7", {"skills": "s1,s3,s4"}), ("v8", {"skills": "s2,s3,s4"})])
    graph3.add_nodes_from([("v9", {"skills": "s1,s4"}), ("v10", {"skills": "s2,s3"}),
                           ("v11", {"skills": "s1,s3"}), ("v12", {"skills": "s2,s4"})])
    graph4.add_nodes_from([("v13", {"skills": "s1"}), ("v14", {"skills": "s2"}),
                           ("v15", {"skills": "s3"}), ("v16", {"skills": "s4"})])
    for graph, tm in zip([graph1, graph2, graph3, graph4], [t1, t2, t3, t4]):
        tm_list = list(graph.nodes)
        graph.add_edge(tm_list[0], tm_list[1])
        graph.add_edge(tm_list[2], tm_list[1])
        graph.add_edge(tm_list[3], tm_list[1])
        tg = graph.subgraph(graph.nodes).copy()
        # show_graph(tg)
        record = ""
        record += str(len(task))
        record += "\t" + str(tm.cardinality())
        record += "\t" + str(team.radius(tg))
        record += "\t" + str(team.diameter(tg))
        record += "\t" + str(team.leader_distance(tg))
        record += "\t" + str(team.leader_skill_distance(tg, task))
        record += "\t" + str(team.sum_distance(tg, task))
        record += "\t" + str(tm.shannon_diversity(tg))
        record += "\t" + str(tm.simpson_density(tg))
        record += "\t" + str(tm.simpson_diversity(tg))
        record += "\t" + str(tm.gini_simpson_diversity(tg))
        print(record)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # toy()
    import networkx as nx
    graph = nx.read_gml("/home/cilab/PycharmProjects/dblp-2015/sigmod.gml")
    skills_name_id_dict = dict()
    # dblp_data = DBLP_Data("2015")
    # with open("/home/cilab/PycharmProjects/dblp-2015/sigmod-titles.txt") as file:
    #     for line in file:
    #         task = dblp_data.get_task_from_title_graph(graph, line.strip("\n").split("\t")[1])
    #         if len(task) > 9:
    with  open("/home/cilab/PycharmProjects/dblp-2015/sigmod-17-tasks-0.txt") as file:
            for line in file:
                # task = dblp_data.get_task_from_title_graph(graph, line.strip("\n").split("\t")[1])
                task = line.strip("\n").split()
                # print(task)
                record = ""
                # task_graph = utilities.get_task_graph(graph, task)
                # largest_cc = task_graph.subgraph(max([cc for cc in nx.connected_components(task_graph)])).copy()
                # nx.draw(largest_cc, with_labels=True)
                # plt.show()
                team = Algorithms.best_sum_distance(graph, task)
                tg = graph.subgraph(team.experts).copy()
                # show_graph(tg)
                record += str(len(task))
                record += "\t" + str(team.cardinality())
                record += "\t" + str(team.radius(tg))
                record += "\t" + str(team.diameter(tg))
                record += "\t" + str(team.leader_distance(tg))
                record += "\t" + str(team.leader_skill_distance(tg, task))
                record += "\t" + str(team.sum_distance(tg, task))
                record += "\t" + str(team.shannon_diversity(tg))
                # record += "\t" + str(team.simpson_density(tg))
                record += "\t" + str(team.simpson_diversity(tg))
                record += "\t" + str(team.gini_simpson_diversity(tg))
                record += "\t" + ",".join(team.experts)
                print(record)

