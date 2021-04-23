def list_to_freq(wordlist) -> dict:
    """
    return dictionary generated from given list
    :param wordlist:
    :return:
    """
    word_freq = dict()
    for word in wordlist:
        if word not in word_freq:
            word_freq[word] = 1
        else:
            word_freq[word] += 1
    return word_freq


# Ref: https://stackoverflow.com/questions/18393842/k-th-order-neighbors-in-graph-python-networkx
def within_k_nbrs(l_gra, start, k):
    nbrs = {start}
    for _ in range(k):
        nbrs = set((nbr for n in nbrs for nbr in l_gra[n]))
    return nbrs

def at_k_nbrs(l_gra, start, k):
    sub = within_k_nbrs(l_gra, start, k)
    sup = within_k_nbrs(l_gra, start, k-1)
    return sub.difference(sup)

# Ref: https://thispointer.com/python-check-if-any-string-is-empty-in-a-list/
def is_empty_or_blank(msg):
    """ This function checks if given string is empty
     or contain only shite spaces"""
    import re
    return re.search("^ *$", msg)


# Ref: https://stackoverflow.com/questions/18393842/k-th-order-neighbors-in-graph-python-networkx
def knbrcover(l_graph, start, k):
    nbrs = within_k_nbrs(l_graph, start, k)
    dnbrs = nbrs.copy()
    hopskillcover = set()
    for n in dnbrs:
        if len(l_graph.nodes[n]) > 0:
            skls = list(filter(None, l_graph.nodes[n]["skills"].split(",")))
            if len(skls) == 0:
                nbrs.remove(n)
            else:
                hopskillcover.update(skls)
    return hopskillcover


def get_expert_skills_dict(graph):
    expert_skills = dict()
    for node in graph.nodes():
        if len(graph.nodes[node]) > 0:
            expert_skills[node] = graph.nodes[node]["skills"].split(",")
    return expert_skills


# ref : https://blog.nelsonliu.me/2016/07/30/progress-bars-for-python-file-reading-with-tqdm/
def get_num_lines(file_path):
    fp = open(file_path, "r+")
    import mmap
    buf = mmap.mmap(fp.fileno(), 0)
    lines = 0
    while buf.readline():
        lines += 1
    return lines


# function to return key for any value
def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key


def remove_numbers_symbols(instring):
    import re
    result1 = re.sub(r'[^\w]', ' ', instring)
    result = ''.join([i for i in result1 if not i.isdigit()])
    return result


def show_mygraph(d_graph):
    import networkx as nx
    import matplotlib.pyplot as plt
    pos = nx.spring_layout(d_graph)  # pos = nx.nx_agraph.graphviz_layout(G)
    nx.draw_networkx(d_graph, pos)
    labels = nx.get_edge_attributes(d_graph, 'weight')
    nx.draw_networkx_edge_labels(d_graph, pos, edge_labels=labels)
    plt.show()

# Ref : https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
def key_with_max_val(dictnry):
    """ a) create a list of the dict's keys and values;
        b) return the key with the max value"""
    v = list(dictnry.values())
    k = list(dictnry.keys())
    return k[v.index(max(v))]

def get_diameter_nodes(l_graph):
    """
    return diameter of graph formed by team
    diam(X) := max{sp_{X}(u,v) | u,v ∈ X}.
    :param l_graph:
    :return:
    """
    import networkx as nx
    # t_graph = self.get_team_graph(l_graph)
    if nx.number_of_nodes(l_graph) < 2:
        return 0
    else:
        spl = dict()
        for nd in l_graph.nodes:
            spl[nd] = nx.single_source_dijkstra_path_length(l_graph, nd)
        eccentrct = nx.eccentricity(l_graph, sp=spl)
        sour = key_with_max_val(eccentrct)  # source
        dest = key_with_max_val(nx.single_source_dijkstra(l_graph, sour)[0])  # destination
        return nx.dijkstra_path(l_graph, sour, dest)