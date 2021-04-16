# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import Algorithms
import utilities
from tqdm import tqdm
# import make_data_file


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # toy()
    import networkx as nx

    # for network in ["vldb", "sigmod", "icde", "icdt", "edbt", "pods", "db"]:
    for network in ["db"]:
        graph = nx.read_gml("/home/cilab/PycharmProjects/dblp-2015/" + network + ".gml")
        skills_name_id_dict = dict()
        # with  open("/home/cilab/PycharmProjects/dblp-2015/" + network + "-titles.txt") as file:
        with open("/home/cilab/PycharmProjects/dblp-2015/" + network + "-17-tasks-0.txt") as file:
            open("/home/cilab/PycharmProjects/dblp-2015/" + network + "-17-tasks-0-results.txt", "w").close()
            n_lines = utilities.get_num_lines("../dblp-2015/" + network + "-17-tasks-0.txt")
            for line in tqdm(file, total=n_lines):
                # task = dblp_data.get_task_from_title_graph(graph, line.strip("\n").split("\t")[1])
                task = line.strip("\n").split()
                # print(task)
                record = ""
                team = Algorithms.rarestfirst(graph, task)
                tg = team.get_leader_team_graph(graph)
                # show_graph(tg)
                record += str(len(task))
                record += "\t" + str(team.cardinality())
                record += "\t" + str(team.radius(tg))
                record += "\t" + str(team.diameter(tg))
                record += "\t" + str(team.leader_distance(tg))
                record += "\t" + str(team.leader_skill_distance(tg, task))
                record += "\t" + str(team.sum_distance(tg, task))
                record += "\t" + str(team.shannon_gamma_task_diversity(tg))
                record += "\t" + str(team.shannon_gamma_team_diversity(tg))
                # record += "\t" + str(team.simpson_density(tg))
                record += "\t" + str(team.simpson_diversity(tg, False))  # task diversity
                record += "\t" + str(team.simpson_diversity(tg, True))
                record += "\t" + str(team.gini_simpson_diversity(tg, False))  # task diversity
                record += "\t" + str(team.gini_simpson_diversity(tg, True))
                record += "\t" + ",".join(team.experts)
                open("/home/cilab/PycharmProjects/dblp-2015/" + network + "-17-tasks-0-results.txt", "a").write(record +
                                                                                                                "\n")
