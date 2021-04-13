# T1-DisC Diversity: Result Diversification based on Dissimilarity and Coverage - 4
# T2-Dense Subgraph Maintenance under Streaming Edge Weight Updates for Real-time Story Identification - 11
# T3-A Unified Approach to Ranking in Probabilistic Databases - 5
# T4-Finding Frequent Items in Data Streams - 5
# T5-Constrained Physical Design Tuning - 4

# import utilities
import networkx as nx
import algorithms
import glob
# import measurements
# import make_data_file
import pickle

# task = utilities.get_task("DisC Diversity: Result Diversification based on Dissimilarity and Coverage")
community = "vldb"
tasks = 17

file_list = sorted(glob.glob("../dblp-2020/" + community + "-" + str(tasks) + "-tasks-[0-4].txt"))
# print("team \t Shanon \t Simpson \t Gini-Simpson\n")
for file_str in file_list:
    open(file_str[:-4] + "-teams-tfs.txt", "wb").close()
    with open(file_str, "r") as file:
        for line in file:
            task = line.strip("\n").split()
            graph = nx.read_gml("../dblp-2020/vldb.gml")
            team = algorithms.tfs(graph, task)
            open(file_str[:-4] + "-teams-tfs.txt", "ab").write(team.leader + "\t" + team.__str__() + "\n")
            # print(team.__str__())
            # if len(team) > 1:
            #     record = str(measurements.shannon_diversity(team, task))
            #     record += " \t" + str(measurements.simpson_diversity(team, task))
            #     record += " \t" + str(measurements.gini_simpson_diversity(team, task))
            #     print(record)
            # else:
            #     print("singleton")

# if __name__ == "__main__":
#     pass
