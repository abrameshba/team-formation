def diversity_toy():
    import Algorithms
    from Team import Team
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
        # show_graph(tg)
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
        print(record)