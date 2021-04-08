def get_skills(publication) -> list:
    """
    returns non trivial words of publication as skills packed in set
    used to get skills of an expert
    non trivial keywords that appear at least twice in his/her publications are skills
    :param publication:
    :return:
    """
    from nltk import word_tokenize
    import re
    from nltk.corpus import stopwords
    all_words = word_tokenize(re.sub(r'[^a-zA-Z]', ' ', publication))
    filtered_words = list()
    skills = set()
    for word in all_words:
        if word not in stopwords.words('english') and len(word) > 2 and word in words.word():
            filtered_words.append(word.lower())
    local_dict = list_to_freq(filtered_words)
    for word, freq in local_dict.items():
        if freq > 1:  # check non trivial words that appear at least twice
            skills.add(word.lower())
    lst = list(skills)
    return sorted(lst)


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


def get_skill_experts_dict(l_graph) -> dict:
    """
    return skill expert community dictionary for input l_graph
    :param l_graph:
    :return dict:
    """
    skill_experts = dict()
    for node in l_graph.nodes():
        if len(l_graph.nodes[node]) > 0:
            for skill in l_graph.nodes[node]["skills"].split(","):
                if skill in skill_experts:
                    skill_experts[skill].append(node)
                elif skill not in skill_experts:
                    skill_experts[skill] = list([node])
                else:
                    pass
    return skill_experts


def get_task(publication) -> list:
    """
    return list of skills(id) of task of parameter
    used to get non-trivial words of parameter(publication) that matched with skills
    :param publication:
    :return:
    """
    from nltk import word_tokenize
    import re
    from nltk.corpus import stopwords
    all_words = word_tokenize(re.sub(r'[^a-zA-Z]', ' ', publication))
    filtered_words = list()
    for word in all_words:
        if word not in stopwords.words('english') and len(word) > 2:
            filtered_words.append(word.lower())
    local_dict = list_to_freq(filtered_words)
    print(filtered_words)
    skills_dict = dict()
    with open("../dblp-2020/vldb-skills.txt", "r") as file:
        for line in file:
            words = line.strip("\n").split()
            skills_dict[words[1]] = words[0]
    task_str = set(local_dict.keys()).intersection(set(skills_dict.keys()))
    task = list()
    for wrd in task_str:
        task.append(skills_dict[wrd])
        print(wrd + "\t" + skills_dict[wrd])
    return list(task)  # returns list of id's of skills


def generate_community_tasks(community, tasks) -> None:
    """
    This method called once, generates community tasks 1700 and 17
    :return:
    """
    import os.path
    import glob
    import random
    import networkx as nx
    max_no = 0

    file_list = glob.glob("../dblp-2020/" + community + "-" + str(tasks) + "-*.txt")
    if len(file_list) >= 5:
        print("please delete existing(old) files")
    elif len(file_list) > 0 :
        max_no = len(file_list)
        file_path = "../dblp-2020/" + community + "-" + str(tasks) + "-tasks-" + str(max_no) + ".txt"
    else:
        file_path = "../dblp-2020/" + community + "-" + str(tasks) + "-tasks-" + str(max_no) + ".txt"
    graph = nx.read_gml("../dblp-2020/" + community + ".gml")
    community_skills = get_community_skills(graph)
    all_tasks = list()
    open(file_path, "w").close()
    if tasks == 17:
        for skills_count in range(4, 21):
            task = set()
            while len(task) < skills_count:
                task.add(random.choice(list(community_skills)))
                if len(task) == skills_count:
                    all_tasks.append(list(task))
            for task in all_tasks:
                for skill in task:
                    open(file_path, "a").write(skill + "\t")
                open(file_path, "a").write("\n")
            all_tasks.clear()
    else:
        for skills_count in range(4, 21):
            for iter_count in range(1, 101):
                task = set()
                while len(task) < skills_count:
                    task.add(random.choice(list(community_skills)))
                    if len(task) == skills_count:
                        all_tasks.append(list(task))
                for task in all_tasks:
                    for skill in task:
                        open(file_path, "a").write(skill + "\t")
                    open(file_path, "a").write("\n")
                all_tasks.clear()


def get_community_skills(graph) -> set:
    """
    skill set of community is returned
    :param graph:
    :return set:
    """
    community_skills = set()
    for node in graph.nodes():
        if len(graph.nodes[node]) > 0:
            for skill in graph.nodes[node]["skills"].split(","):
                if len(skill) > 0:
                    community_skills.add(skill)
    return community_skills

#Ref: https://stackoverflow.com/questions/18393842/k-th-order-neighbors-in-graph-python-networkx
def knbrs(G, start, k):
    nbrs = set([start])
    for l in range(k):
        nbrs = set((nbr for n in nbrs for nbr in G[n]))
    return nbrs

#Ref: https://thispointer.com/python-check-if-any-string-is-empty-in-a-list/
def is_empty_or_blank(msg):
    """ This function checks if given string is empty
     or contain only shite spaces"""
    import re
    return re.search("^\s*$", msg)

#Ref: https://stackoverflow.com/questions/18393842/k-th-order-neighbors-in-graph-python-networkx
def knbrcover(l_graph, start, k):
    nbrs = knbrs(l_graph, start, k)
    dnbrs = nbrs.copy()
    hopskillcover = set()
    for n in dnbrs:
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