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
def knbrs(l_gra, start, k):
    nbrs = {start}
    for _ in range(k):
        nbrs = set((nbr for n in nbrs for nbr in l_gra[n]))
    return nbrs


# Ref: https://thispointer.com/python-check-if-any-string-is-empty-in-a-list/
def is_empty_or_blank(msg):
    """ This function checks if given string is empty
     or contain only shite spaces"""
    import re
    return re.search("^ *$", msg)


# Ref: https://stackoverflow.com/questions/18393842/k-th-order-neighbors-in-graph-python-networkx
def knbrcover(l_graph, start, k):
    nbrs = knbrs(l_graph, start, k)
    dnbrs = nbrs.copy()
    hopskillcover = set()
    for n in dnbrs:
        if len(l_graph.nodes[n])>0:
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
