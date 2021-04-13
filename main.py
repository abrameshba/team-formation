# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# import make_data_file
import utilities
import measurements


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

    graph = nx.read_gml("../dblp-2020/vldb.gml")
    # open("../dblp-2020/vldb-17-tasks-1-rf-stats.txt", "w").close()
    with open("../dblp-2020/vldb-17-tasks-4-teams-tfs.txt", "r") as file:
        # print("task_size\tteam_size\tradius\tdiameter\tld\tlsd\tsd\shndiv\tsimpdiv\tginidiv\n")
        for line in file:
            task = list()
            spw = line.strip("\n").split("\t")
            team = Team()
            team.leader = spw[0]
            team_str = spw[1].strip(" ").split(" ")
            for mmbr in team_str:
                expert = mmbr.split(":")[0]
                skills = mmbr.split(":")[1].split(",")
                team.experts.add(expert)
                team.skills[expert] = list()
                for skill in skills:
                    team.skills[expert].append(skill)
                    task.append(skill)
            record = ""
            record += str(len(task))
            record += "\t" + str(team.cardinality())
            record += "\t" + str(team.radius(graph))
            record += "\t" + str(team.diameter(graph))
            record += "\t" + str(round(team.leader_distance(graph), 2))
            record += "\t" + str(round(team.leader_skill_distance(graph, task), 2))
            record += "\t" + str(round(team.sum_distance(graph, task), 2))
            # record += "\t" + str(format(team.shannon_diversity(team, task), "1.2f"))
            # record += "\t" + str(format(team.simpson_density(team, task), "1.2f"))
            # record += "\t" + str(format(team.simpson_diversity(team, task), "1.2f"))
            # record += "\t" + str(format(team.gini_simpson_diversity(team, task), "1.2f"))
            print(record)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
