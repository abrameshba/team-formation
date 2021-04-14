# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# import make_data_file
import utilities
import measurements
import Algorithms
import matplotlib.pyplot as plt


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def show_graph(d_graph):
    plt.clf()
    pos = nx.spring_layout(d_graph)  # pos = nx.nx_agraph.graphviz_layout(G)
    nx.draw_networkx(d_graph, pos)
    labels = nx.get_edge_attributes(d_graph, 'weight')
    nx.draw_networkx_edge_labels(d_graph, pos, edge_labels=labels)
    plt.show()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # #print_hi('PyCharm')
    # make_data_file.make_data_file("vldb")
    # for cnt in range(0, 5):
    #     utilities.generate_community_tasks("vldb", 17)
    #     utilities.generate_community_tasks("vldb", 1700)
    import networkx as nx
    from Team import Team

    graph = nx.read_gml("/home/cilab/PycharmProjects/dblp-2015/sigmod.gml")
    # open("../dblp-2020/vldb-17-tasks-1-rf-stats.txt", "w").close()
    # task = ["A", "B", "C", "D"]
    skills_name_id_dict = dict()
    with open("../dblp-2015/sigmod-skills.txt", "r") as file:
        for line in file:
            line_words = line.strip("\n").split("\t")
            skills_name_id_dict[line_words[1]] = line_words[0]
        del line_words, line
    with open("/home/cilab/PycharmProjects/dblp-2015/sigmod-titles.txt") as file:
        for line in file:
            task = utilities.get_task_from_title_graph(graph, line.strip("\n").split("\t")[1])
            if len(task) > 7 :
                print(line)
                record = ""
                # task_graph = utilities.get_task_graph(graph, task)
                # largest_cc = task_graph.subgraph(max([cc for cc in nx.connected_components(task_graph)])).copy()
                # nx.draw(largest_cc, with_labels=True)
                # plt.show()
                team, all_exps = Algorithms.rarestfirst(graph, task)
                tsg = graph.subgraph(all_exps).copy()
                show_graph(tsg)
                tg = graph.subgraph(team.experts).copy()
                # show_graph(tg)
                record += str(len(task))
                record += "\t" + str(team.cardinality())
                record += "\t" + str(team.radius(tg))
                record += "\t" + str(team.diameter(tg))
                record += "\t" + str(round(team.leader_distance(tg), 2))
                record += "\t" + str(round(team.leader_skill_distance(tg, task), 2))
                record += "\t" + str(round(team.sum_distance(tg, task), 2))
                print()
                print(team)
                # record += "\t" + str(format(team.shannon_diversity(team, task), "1.2f"))
                # record += "\t" + str(format(team.simpson_density(team, task), "1.2f"))
                # record += "\t" + str(format(team.simpson_diversity(team, task), "1.2f"))
                # record += "\t" + str(format(team.gini_simpson_diversity(team, task), "1.2f"))
                print(record)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
