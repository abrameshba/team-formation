def rarestfirst(l_graph, l_task):
    """
    returns team of experts with minimum diameter distance
    :param l_graph:
    :param l_task:
    :return tuple(set, dictionary, string):
    """
    import utilities
    from Team import Team
    import measurements
    import networkx as nx
    l_skill_expert = utilities.get_skill_experts_dict(l_graph)
    rare_skills_support = [min([(len(l_skill_expert[l_skill]), l_skill) for l_skill in l_task], key=lambda x: x[0])]
    rare_skills = [l_skill for count, l_skill in rare_skills_support]
    min_dd = 100  # minimum diameter distance
    best_team = Team()
    for rare_skill in rare_skills:
        for candidate in l_skill_expert[rare_skill]:
            team = Team()
            team.leader = candidate
            team.experts.add(candidate)
            if candidate not in team.skills.keys():
                team.skills[candidate] = list()
                team.skills[candidate].append(rare_skill)
            else:
                team.skills[candidate].append(rare_skill)
            for l_skill in l_task:
                closest_expert = ""
                if rare_skill != l_skill:
                    min_distance = 100
                    for expert in l_skill_expert[l_skill]:
                        if expert in l_graph and candidate in l_graph and nx.has_path(l_graph, candidate,
                                                                                      expert):
                            distance = nx.dijkstra_path_length(l_graph, candidate, expert, weight="weight")
                            if min_distance > distance:
                                min_distance = distance
                                closest_expert = (expert + ".")[:-1]
                            else:
                                pass
                        else:
                            pass
                    if len(closest_expert) > 0:
                        team.experts.add(closest_expert)
                        if closest_expert not in team.skills:
                            team.skills[closest_expert] = list()
                            team.skills[closest_expert].append(l_skill)
                        else:
                            team.skills[closest_expert].append(l_skill)
            team_graph = team.get_team_graph(l_graph)
            dd = team.diameter(team_graph)
            print(team)
            if dd is not None:
                if min_dd > dd:
                    min_dd = dd
                    best_team = team
    return best_team


def best_sum_distance(l_graph, l_task):
    """
    returns team of experts with minimum sum distance
    :param l_graph:
    :param l_task:
    :return tuple(set, dictionary, string):
    """
    import utilities
    import measurements
    from Team import Team
    import networkx as nx
    l_skill_expert = utilities.get_skill_experts_dict(l_graph)
    least_sum_distance = 10000
    best_team = Team()
    for skill_i in l_task:
        for candidate in l_skill_expert[skill_i]:
            team = Team()
            team.leader = candidate
            team.experts.add(candidate)
            if candidate not in team.skills:
                team.skills[candidate] = list()
                team.skills[candidate].append(skill_i)
            else:
                team.skills[candidate].append(skill_i)
            for skill_j in l_task:
                if skill_i != skill_j:
                    min_dis = 100
                    closest_expert = ""
                    for expert in l_skill_expert[skill_j]:
                        if nx.has_path(l_graph, candidate, expert):
                            dis = nx.dijkstra_path_length(l_graph, candidate, expert, weight="weight")
                            if min_dis > dis:
                                min_dis = dis
                                closest_expert = (expert + ".")[:-1]
                    if len(closest_expert) > 0:
                        team.experts.add(closest_expert)
                        if closest_expert not in team.skills:
                            team.skills[closest_expert] = list()
                            team.skills[closest_expert].append(skill_j)
                        else:
                            team.skills[closest_expert].append(skill_j)
            sum_dist = team.sum_distance(l_graph, l_task)
            print(team)
            if sum_dist < least_sum_distance:
                least_sum_distance = sum_dist
                best_team = team
    return best_team


def tfs(l_graph, l_task):  # twice of average degree
    """
    return community based team formation using closest expert.
    :param l_graph:
    :param l_task:
    :return:
    """
    import random
    import measurements
    from Team import Team
    import utilities
    import networkx as nx
    # rds = nx.radius(l_graph)
    avg_degree = (2 * l_graph.number_of_edges()) / float(l_graph.number_of_nodes())
    hc = sorted([n for n, d in l_graph.degree() if len(l_graph.nodes[n]) > 0 and
                 d >= avg_degree and
                 len(set(l_graph.nodes[n]["skills"].split(",")).intersection(set(l_task))) > 0],
                reverse=True)
    best_team = Team()
    team = Team()
    best_ldr_distance = 1000
    expert_skills = utilities.get_expert_skills_dict(l_graph)
    skill_experts = utilities.get_skill_experts_dict(l_graph)
    random_expert_added = 0
    print(hc)
    for c_node in hc:
        task_copy = l_task[:]
        hops = 1
        while hops < 3 and len(task_copy) > 0:
            team = Team()
            task_copy = l_task[:]
            random_expert_added = 0
            team.leader = c_node
            skill_cover = set(task_copy).intersection(
                set(l_graph.nodes[team.leader]["skills"].split(",")))  # expert skills matched with l_task
            team.experts.add(c_node)
            if c_node not in team.skills:
                team.skills[c_node] = list()
                for skill in skill_cover:
                    team.skills[c_node].append(skill)
            else:
                for skill in skill_cover:
                    team.skills[c_node].append(skill)
            for skill in skill_cover:
                if skill in task_copy:
                    task_copy.remove(skill)
            task_covered = utilities.knbrcover(l_graph, team.leader, hops).intersection(
                task_copy)  # hop neighbour hood skill coverage
            neighbors = utilities.knbrs(l_graph, team.leader, hops)  # hop neighbours
            while len(task_covered) > 0:
                neighborhood = list()
                for node in neighbors:
                    node_covered_skills = set()
                    if node in expert_skills:
                        node_covered_skills = set(expert_skills[node]).intersection(task_copy)
                    if len(node_covered_skills) > 0:
                        neighborhood.append([node, node_covered_skills,
                                             nx.dijkstra_path_length(l_graph, team.leader, node, weight="weight")])
                neighborhood.sort(
                    key=lambda elem: (-len(elem[1]), elem[2]))  # sort neighbor hood max skills and min distance
                team.experts.add(neighborhood[0][0])  # first element of neighbor hood
                if neighborhood[0][0] not in team.skills:
                    team.skills[neighborhood[0][0]] = list()
                    for skill in neighborhood[0][1]:
                        team.skills[neighborhood[0][0]].append(skill)
                else:
                    for skill in skill_cover:
                        team.skills[neighborhood[0][0]].append(skill)
                neighbors.remove(neighborhood[0][0])
                for skl in neighborhood[0][1]:
                    if skl in task_copy:
                        task_copy.remove(skl)
                    if skl in task_covered:
                        task_covered.remove(skl)
            if len(task_copy) == 0:
                break
            hops += 1
        while len(task_copy) > 0:
            skl = random.choice(task_copy)
            min_dis = 100
            close_expert = ""
            for expert in skill_experts[skl]:
                if nx.has_path(l_graph, team.leader, expert):
                    dis = nx.dijkstra_path_length(l_graph, team.leader, expert, weight="weight")
                    if min_dis > dis:
                        min_dis = dis
                        close_expert = (expert + ".")[:-1]
            team.experts.add(close_expert)  # first element of neighbor hood
            if close_expert not in team.skills:
                team.skills[close_expert] = list()
                team.skills[close_expert].append(skl)
            else:
                team.skills[close_expert].append(skl)
            task_copy.remove(skl)
            random_expert_added += 1
        if len(task_copy) > 0:
            continue
        elif len(task_copy) == 0:
            # print(i, team)
            ld = team.leader_distance(l_graph)
            if best_ldr_distance > ld:
                best_ldr_distance = ld
                best_team = team
        else:
            pass
    return best_team


def tfc(l_graph, l_task):  # twice of average degree
    """
    return community based team formation using closest expert.
    :param l_graph:
    :param l_task:
    :return:
    """
    import random
    import measurements
    from Team import Team
    import utilities
    import networkx as nx
    # rds = nx.radius(l_graph)
    avg_degree = (2 * l_graph.number_of_edges()) / float(l_graph.number_of_nodes())
    hc = sorted([n for n, d in l_graph.degree() if len(l_graph.nodes[n]) > 0 and
                 d >= avg_degree and
                 len(set(l_graph.nodes[n]["skills"].split(",")).intersection(set(l_task))) > 0],
                reverse=True)
    best_team = Team()
    team = Team()
    best_ldr_distance = 1000
    expert_skills = utilities.get_expert_skills_dict(l_graph)
    skill_experts = utilities.get_skill_experts_dict(l_graph)
    random_expert_added = 0
    print(hc)
    for c_node in hc:
        task_copy = l_task[:]
        hops = 1
        while hops < 3 and len(task_copy) > 0:
            team = Team()
            task_copy = l_task[:]
            random_expert_added = 0
            team.leader = c_node
            skill_cover = set(task_copy).intersection(
                set(l_graph.nodes[team.leader]["skills"].split(",")))  # expert skills matched with l_task
            team.experts.add(c_node)
            if c_node not in team.skills:
                team.skills[c_node] = list()
                for skill in skill_cover:
                    team.skills[c_node].append(skill)
            else:
                for skill in skill_cover:
                    team.skills[c_node].append(skill)
            for skill in skill_cover:
                if skill in task_copy:
                    task_copy.remove(skill)
            task_covered = utilities.knbrcover(l_graph, team.leader, hops).intersection(
                task_copy)  # hop neighbour hood skill coverage
            neighbors = utilities.knbrs(l_graph, team.leader, hops)  # hop neighbours
            while len(task_covered) > 0:
                neighborhood = list()
                for node in neighbors:
                    node_covered_skills = set()
                    if node in expert_skills:
                        node_covered_skills = set(expert_skills[node]).intersection(task_copy)
                    if len(node_covered_skills) > 0:
                        neighborhood.append([node, node_covered_skills,
                                             nx.dijkstra_path_length(l_graph, team.leader, node, weight="weight")])
                neighborhood.sort(
                    key=lambda elem: (-len(elem[1]), elem[2]))  # sort neighbor hood max skills and min distance
                team.experts.add(neighborhood[0][0])  # first element of neighbor hood
                if neighborhood[0][0] not in team.skills:
                    team.skills[neighborhood[0][0]] = list()
                    for skill in neighborhood[0][1]:
                        team.skills[neighborhood[0][0]].append(skill)
                else:
                    for skill in skill_cover:
                        team.skills[neighborhood[0][0]].append(skill)
                neighbors.remove(neighborhood[0][0])
                for skl in neighborhood[0][1]:
                    if skl in task_copy:
                        task_copy.remove(skl)
                    if skl in task_covered:
                        task_covered.remove(skl)
            if len(task_copy) == 0:
                break
            hops += 1
        while len(task_copy) > 0:
            skl = random.choice(task_copy)
            random_expert = random.choice(skill_experts[skl])
            team.experts.add(random_expert)
            if random_expert not in team.skills:
                team.skills[random_expert] = list()
                team.skills[random_expert].append(skl)
            else:
                team.skills[random_expert].append(skl)
            task_copy.remove(skl)
            random_expert_added += 1
        if len(task_copy) > 0:
            continue
        elif len(task_copy) == 0:
            # print(i, team)
            ld = team.leader_distance(l_graph)
            if best_ldr_distance > ld:
                best_ldr_distance = ld
                best_team = team
        else:
            pass
    return best_team


def best_leader_distance(l_graph, l_task):
    """
    returns team of experts with minimum leader distance
    :param l_graph:
    :param l_task:
    :return Team :
    """
    import utilities
    import measurements
    import networkx as nx
    from Team import Team
    l_skill_expert = utilities.get_skill_experts_dict(l_graph)
    ldr_distance = 1000
    best_team = Team()
    for candidate in nx.nodes(l_graph):
        team = Team()
        team.leader = candidate
        team.experts.add(candidate)
        skill_cover = set(l_task).intersection(
            set(l_graph.nodes[team.leader]["skills"].split(",")))  # expert skills matched with l_task
        for skill in skill_cover:
            if candidate not in team.skills:
                team.skills[candidate] = list()
                team.skills[candidate].append(skill)
            else:
                team.skills[candidate].append(skill)
        r_skills = set(l_task).difference(skill_cover)
        for skill in r_skills:
            min_dis = 100
            closest_expert = ""
            for expert in l_skill_expert[skill]:
                if nx.has_path(l_graph, candidate, expert):
                    dis = nx.dijkstra_path_length(l_graph, candidate, expert, weight="weight")
                    if min_dis > dis:
                        min_dis = dis
                        closest_expert = (expert + ".")[:-1]
            if len(closest_expert) > 0:
                team.experts.add(closest_expert)
                if closest_expert not in team.skills:
                    team.skills[closest_expert] = list()
                    team.skills[closest_expert].append(skill)
                else:
                    team.skills[closest_expert].append(skill)
        print(team)
        cld = team.leader_skill_distance(l_graph, l_task)
        if ldr_distance > cld:
            ldr_distance = cld
            best_team = team
    return best_team


def min_diam_sol(l_graph, l_task, user, hops) -> (dict, str):
    """
    Return team generated by Minimum diameter solution algorithm
    :param l_graph:
    :param l_task:
    :param user:
    :param hops:
    :return:
    """
    ldnodes = list()
    for node in l_graph.nodes:
        if nx.dijkstra_path_length(l_graph, user, node) <= hops:
            ldnodes.append(node)
        else:
            pass
    pgraph = nx.subgraph(l_graph, ldnodes).copy()  # processed graph excluding given hops away nodes from user
    for r in range(hops):
        hopnodes = utilities.knbrs(pgraph, user, r)
        dhopnodes = hopnodes.copy()
        hopskillcover = set()
        for n in dhopnodes:
            skls = list(filter(None, l_graph.nodes[n]["skills"].split(",")))
            if len(skls) == 0:
                hopnodes.remove(n)
            else:
                hopskillcover.update(skls)
        if len(hopskillcover.intersection(set(l_task))) == len(l_task):
            print(hopnodes)
            print(r)
            break


if __name__ == "__main__":
    import networkx as nx
    import utilities
    import random

    graph = nx.read_gml("../dblp-2020/vldb.gml")
    task = utilities.get_task("DisC Diversity: Result Diversification based on Dissimilarity and Coverage")
    users = set()
    aln = [n for n in graph.nodes]
    for u in range(5):
        users.add(random.choice(aln))
    for u in users:
        print(u)
        min_diam_sol(graph, task, u, nx.radius(graph))  # h = 5
