# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# import make_data_file
import utilities
import measurements
import Algorithms

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # #print_hi('PyCharm')
    # make_data_file.make_data_file("vldb")
    # for cnt in range(0, 5):
    #     utilities.generate_community_tasks("vldb", 17)
    #     utilities.generate_community_tasks("vldb", 1700)
    import networkx as nx
    from Team import Team

    graph = nx.read_gml("/home/cilab/paper-1/network.gml")
    # open("../dblp-2020/vldb-17-tasks-1-rf-stats.txt", "w").close()
    task = ["A", "B", "C", "D"]
    record = ""
    team = Algorithms.tfc(graph, task)
    record += str(len(task))
    record += "\t" + str(team.cardinality())
    record += "\t" + str(team.radius(graph))
    record += "\t" + str(team.diameter(graph))
    record += "\t" + str(round(team.leader_distance(graph), 2))
    record += "\t" + str(round(team.leader_skill_distance(graph, task), 2))
    record += "\t" + str(round(team.sum_distance(graph, task), 2))
    print()
    print(team)
    # record += "\t" + str(format(team.shannon_diversity(team, task), "1.2f"))
    # record += "\t" + str(format(team.simpson_density(team, task), "1.2f"))
    # record += "\t" + str(format(team.simpson_diversity(team, task), "1.2f"))
    # record += "\t" + str(format(team.gini_simpson_diversity(team, task), "1.2f"))
    print(record)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
