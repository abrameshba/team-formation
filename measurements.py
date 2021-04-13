def shannon_diversity(l_team, l_task):
    """
    returns Shannon entropy
    :param l_team:
    :param l_task:
    :return:
    """
    import math
    author_skills_dict = dict()
    with open("../dblp-2020/vldb-authors-skills.txt", "r") as file:
        for line in file:
            words = line.strip("\n").split()
            author_skills_dict[words[0]] = words[1]
    shannon_sum = 0
    for ts in l_task:
        cn = 0
        for member in l_team.experts:
            if member in author_skills_dict and ts in author_skills_dict[member]:
                cn += 1
        prob = cn / len(l_team.experts)
        shannon_sum += prob * math.log(prob)
    # print(pow(math.e, -1 * shannon_sum))
    # shannon_sum = 0
    # tot_skls = set()
    # for member in l_team.experts:
    #     tot_skls.update(set(author_skills_dict[member].split(",")))
    # for ts in tot_skls:
    #     cn = 0
    #     for member in l_team.experts:
    #         if member in author_skills_dict and ts in author_skills_dict[member]:
    #             cn += 1
    #     prob = cn / len(l_team.experts)
    #     shannon_sum += prob * math.log(prob)
    # print(pow(math.e, -1 * shannon_sum))
    return pow(math.e, -1 * shannon_sum)


def simpson_density(l_team, l_task):
    """
    calculates reciprocal simpson diversity
    :return:
    """
    author_skills_dict = dict()
    with open("../dblp-2020/vldb-authors-skills.txt", "r") as file:
        for line in file:
            words = line.strip("\n").split()
            author_skills_dict[words[0]] = words[1]
    simpson_sum = 0
    for ts in l_task:
        cn = 0
        for member in l_team.experts:
            if member in author_skills_dict and ts in author_skills_dict[member]:
                cn += 1
        prob = cn / len(l_team.experts)
        simpson_sum += pow(prob, 2)
    # simpson_sum = 0
    # tot_skls = set()
    # for member in l_team.experts:
    #     tot_skls.update(set(author_skills_dict[member].split(",")))
    # for ts in tot_skls:
    #     cn = 0
    #     for member in l_team.experts:
    #         if member in author_skills_dict and ts in author_skills_dict[member]:
    #             cn += 1
    #     prob = cn / len(l_team.experts)
    #     simpson_sum += pow(prob, 2)
    return simpson_sum


def simpson_diversity(l_team, l_task):
    return 1 / simpson_density(l_team, l_task)


def gini_simpson_diversity(l_team, l_task):
    return 1 - simpson_density(l_team, l_task)
