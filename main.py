# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# import make_data_file
# import utilities
# import measurements


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    import networkx as nx
    # from Team import Team
    import Algorithms

    graph = nx.read_gml("../dblp-2015/sigmod.gml")
    with open("../dblp-2015/sigmod-17-tasks-0.txt", "r") as file:
        for line in file:
            task = line.strip("\n").split()
            team = Algorithms.rarestfirst(graph, task)
            team_graph = graph.subgraph(team.experts).copy()
            record = ""
            record += str(len(task))
            record += "\t" + str(team.cardinality())
            record += "\t" + str(team.radius(team_graph))
            record += "\t" + str(team.diameter(team_graph))
            record += "\t" + str(team.leader_distance(team_graph))
            record += "\t" + str(team.leader_skill_distance(team_graph, task))
            record += "\t" + str(team.sum_distance(team_graph, task))
            # record += "\t" + str(format(team.shannon_diversity(team, task), "1.2f"))
            # record += "\t" + str(format(team.simpson_density(team, task), "1.2f"))
            # record += "\t" + str(format(team.simpson_diversity(team, task), "1.2f"))
            # record += "\t" + str(format(team.gini_simpson_diversity(team, task), "1.2f"))
            print(record)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
