# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from tqdm import tqdm

import Algorithms
import utilities


def main_run(algori):
    import networkx as nx
    from Team import Team
    year = "2015"
    # for network in ["db"]:
    networks = ["vldb", "icde", "icdt", "edbt", "pods", "sigmod", "db"]
    for network in tqdm(networks):
        graph = nx.read_gml("../dblp-" + year + "/" + network + ".gml")
        # skills_name_id_dict = dict()
        # with  open("../dblp-" + year + "/" + network + "-titles.txt") as file:
        with open("../dblp-" + year + "/" + network + "-17-tasks-0.txt") as file:
            open("../dblp-" + year + "/" + network + "-17-tasks-0-" + algori + "-results.txt", "w").close()
            open("../dblp-" + year + "/" + network + "-17-tasks-0-" + algori + "-teams.txt", "w").close()
            n_lines = utilities.get_num_lines("../dblp-" + year + "/" + network + "-17-tasks-0.txt")
            for line in tqdm(file, total=n_lines):
                # task = dblp_data.get_task_from_title_graph(graph, line.strip("\n").split("\t")[1])
                task = line.strip("\n").split()
                # print(task)
                record = ""
                team = Team()
                if algori == "rfs":
                    team = Algorithms.rarestfirst(graph, task)
                elif algori == "tfs":
                    team = Algorithms.tfs(graph, task)
                elif algori == "bsd":
                    team = Algorithms.best_sum_distance(graph, task)
                else:
                    print("No Algorithms selected, exiting")
                    exit(0)
                tg = team.get_team_graph(graph)
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
                open("../dblp-" + year + "/" + network + "-17-tasks-0-" + algori + "-results.txt", "a").write(
                    record + "\n")
                open("../dblp-" + year + "/" + network + "-17-tasks-0-" + algori + "-teams.txt", "a").write(
                    ",".join(sorted(team.experts)) + "\n")


def multiprocessing_func(algo):
    main_run(algo)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import multiprocessing
    import time

    start_time = time.time()
    processes = []
    for alg in ["rfs", "tfs", "bsd"]:
        p = multiprocessing.Process(target=multiprocessing_func, args=(alg,))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()
    tqdm.write('Time taken = {} seconds'.format(time.time() - start_time))
