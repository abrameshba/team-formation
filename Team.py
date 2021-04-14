class Team:

    def __init__(self):
        self.experts = set()
        self.skills = dict()
        self.record = ""
        self.leader = ""
        self.close_experts = set()

    def __str__(self):  # real signature unknown
        """ Return str(self). """
        # if self.cardinality()==0:
        self.record = ""
        if len(self.experts) == 0:
            self.record = "Team Not Yet Formed"
        for expert in self.experts:
            self.record += " " + expert + ":" + ",".join(self.skills[expert])
        return self.record

    def cardinality(self):
        return len(self.experts)

    def get_team_graph(self, l_graph):
        """
        return graph formed by team
        :param l_graph:
        :return:
        """
        nodes = set()
        import networkx as nx
        for nd1 in self.experts:
            for nd2 in self.experts:
                if nd1 != nd2:
                    if nx.has_path(l_graph, nd1, nd2):
                        for node in nx.dijkstra_path(l_graph, nd1, nd2):
                            nodes.add(node)
        return l_graph.subgraph(nodes).copy()

    def diameter(self, l_graph) -> float:
        """
        return diameter of graph formed by team
        diam(G) := max{dist_{G,w}(u,v) | u ∈ V(G),v ∈ V(G)}.
        :param l_graph:
        :return:
        """
        import networkx as nx
        t_graph = self.get_team_graph(l_graph)
        if nx.number_of_nodes(t_graph) < 2:
            return 0
        else:
            sp = dict()
            for nd in t_graph.nodes:
                sp[nd] = nx.single_source_dijkstra_path_length(t_graph,nd)
            e = nx.eccentricity(t_graph, sp=sp)
            return nx.diameter(t_graph, e)

    def radius(self, l_graph) -> float:
        """
        return diameter of graph formed by team
        :param l_graph:
        :return:
        """
        import networkx as nx
        t_graph = self.get_team_graph(l_graph)
        if nx.number_of_nodes(t_graph) < 2:
            return 0
        else:
            sp = dict()
            for nd in t_graph.nodes:
                sp[nd] = nx.single_source_dijkstra_path_length(t_graph,nd)
            e = nx.eccentricity(t_graph, sp=sp)
            return nx.radius(t_graph, e)

    def sum_distance(self, l_graph, task) -> float:
        """
        returns sum of pair wise skills distance of task
        :param l_graph:
        :param task:
        :return:
        """
        import networkx as nx
        # from Team import Team
        sd = 0
        expert_i = expert_j = ""
        for skill_i in task:
            for skill_j in task:
                if skill_i != skill_j:
                    for member in self.experts:
                        if skill_i in self.skills[member]:
                            expert_i = member
                        if skill_j in self.skills[member]:
                            expert_j = member
                    if expert_i in l_graph and expert_j in l_graph and nx.has_path(l_graph, expert_i, expert_j):
                        sd += nx.dijkstra_path_length(l_graph, expert_i, expert_j, weight="weight")
        sd /= 2
        return sd

    def leader_skill_distance(self, l_graph, l_task) -> float:
        """
        return leader skill distance of team i.e. (skills of leader, skill responsible team_member) pairs
        :param l_graph:
        :param l_task:
        :return:
        """
        import networkx as nx
        # from Team import Team
        ld = 0
        if len(self.experts) < 2:
            return 0
        else:
            for skill in l_task:
                for member in self.experts:
                    if member in self.experts and skill in self.skills[member]:
                        if nx.has_path(l_graph, self.leader, member):
                            ld += nx.dijkstra_path_length(l_graph, self.leader, member, weight="weight")
                            continue
        return ld

    def leader_distance(self, l_graph) -> float:
        """
        return leader distance of team i.e. (leader, team_member) pairs
        :param l_graph:
        :return:
        """
        import networkx as nx
        ld = 0
        if len(self.experts) < 2:
            return 0
        else:
            for member in self.experts:
                if member != self.leader:
                    if nx.has_path(l_graph, self.leader, member):
                        ld += nx.dijkstra_path_length(l_graph, self.leader, member, weight="weight")
        return ld


if __name__ == "__main__":
    team = Team()
    import sys

    print("memory required in bytes : " + str(team.__sizeof__()))                       #   sizeof
    print("memory required in bytes with overhead : " + str(sys.getsizeof(team)))       #   sizeof with overhead
    print("string " + team.__str__())
    print("cardinality " + str(team.cardinality()))
