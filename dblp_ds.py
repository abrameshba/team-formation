import multiprocessing
import time

from tqdm import tqdm


# class DBLPRecord:
#
#     def __init__(self):
#         self.title = ""
#         self.authors = set()
#         self.year = ""
#         self.journal = ""


# def get_task_graph(l_graph, l_task):
#     """
#     return subgraph experts with shortest paths among
#     :param l_task:
#     :param l_graph:
#     :return dict:
#     """
#     task_experts = set()
#     skill_set = set(l_task)
#     for node in l_graph.nodes():
#         if len(l_graph.nodes[node]) > 0:
#             if len(set(l_graph.nodes[node]["skills"].split(",")).intersection(skill_set)) > 0:
#                 task_experts.add(node)
#     return l_graph.subgraph(task_experts).copy()


# def get_skill_experts_dict(l_graph) -> dict:
#     """
#     return skill expert community dictionary for input l_graph
#     :param l_graph:
#     :return dict:
#     """
#     skill_experts = dict()
#     for node in l_graph.nodes():
#         if len(l_graph.nodes[node]) > 0:
#             for skill in l_graph.nodes[node]["skills"].split(","):
#                 if skill in skill_experts:
#                     skill_experts[skill].append(node)
#                 elif skill not in skill_experts:
#                     skill_experts[skill] = list([node])
#                 else:
#                     pass
#     return skill_experts


def get_cmnt_skills(publication) -> list:
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
    filtered_words = set()
    from nltk.corpus import brown
    setofwords = set(brown.words())
    for word in all_words:
        if word.lower() not in stopwords.words('english') and len(word) > 2:
            filtered_words.add(word.lower())
    lst = list(filtered_words.intersection(setofwords))
    return sorted(lst)


def get_dblp_skills(publication) -> list:
    """
    returns non trivial words of publication as skills packed in set
    used to get skills of an expert
    non trivial keywords that appear at least twice in his/her publications are skills
    :param publication:
    :return:
    """
    from nltk import word_tokenize
    import re
    import utilities
    from nltk.corpus import stopwords
    all_words = word_tokenize(re.sub(r'[^a-zA-Z]', ' ', publication))
    filtered_words = list()
    skills = set()
    from nltk.corpus import brown
    setofwords = set(brown.words())
    for word in all_words:
        if word.lower() not in stopwords.words('english') and len(word) > 2:
            filtered_words.append(word.lower())
    local_dict = utilities.list_to_freq(filtered_words)
    for word, freq in local_dict.items():
        if freq > 1 and word in setofwords:  # check non trivial words that appear at least twice
            skills.add(word.lower())
    lst = list(skills)
    return sorted(lst)


class DBLP_Data:

    def __init__(self, year):
        self.year = year

    def write_authors_info(self, network):
        """
        if network id dblp
        This function reads a file ../dblp-year/dblp.txt
        extracts name of the authors, builds a dictionary, assigns unique id to each author.
        writes dictionary to a  file ../dblp-year/dblp-authors.txt
        else
        reads a file ../dblp-year/dblp-authors.txt
        for authors belongs to network with
        writes dictionary to a file ../dblp-year/network-authors.txt
        :return:
        """
        import utilities
        if network == "db":
            authors_name_set = set()
            with open("../dblp-" + self.year + "/" + network + ".txt") as file:
                n_lines = utilities.get_num_lines("../dblp-" + self.year + "/" + network + ".txt")
                tqdm.write("processing ../dblp-" + self.year + "/" + network + ".txt - authors info ")
                for line in tqdm(file, total=n_lines):
                    if "<author>" in line:
                        authors = line[line.index("<author>") + len("<author>"):line.index("</author>")].split(":")
                        for author in authors:
                            if author not in authors_name_set:
                                authors_name_set.add(author)
                            else:
                                pass
            author_id = 1
            author_id_name_dict = dict()
            author_name_id_dict = dict()
            open("../dblp-" + self.year + "/" + network + "-authors.txt", "w").close()
            tqdm.write("writing ../dblp-" + self.year + "/" + network + "-authors.txt -  authors info ")
            for author in tqdm(authors_name_set, total=len(authors_name_set)):
                author_id_name_dict[author_id] = author
                author_name_id_dict[author] = author_id
                open("../dblp-" + self.year + "/" + network + "-authors.txt", "a").write(
                    str(author_id) + "\t" + author + "\n")
                author_id += 1
        else:
            dblp_author_name_id_dict = dict()
            with open("../dblp-" + self.year + "/db-authors.txt", "r") as file:
                for line in file:
                    words = line.strip("\n").split("\t")
                    dblp_author_name_id_dict[words[1]] = words[0]
            author_name_id_dict = dict()
            with open("../dblp-" + self.year + "/" + network + ".txt") as file:
                n_lines = utilities.get_num_lines("../dblp-" + self.year + "/" + network + ".txt")
                tqdm.write("processing ../dblp-" + self.year + "/" + network + ".txt - authors info ")
                for line in tqdm(file, total=n_lines):
                    if "<author>" in line:
                        authors = line[line.index("<author>") + len("<author>"):line.index("</author>")].split(":")
                        for author in authors:
                            if author not in author_name_id_dict:
                                author_name_id_dict[author] = dblp_author_name_id_dict[author]
            open("../dblp-" + self.year + "/" + network + "-authors.txt", "w").close()
            tqdm.write("writing ../dblp-" + self.year + "/" + network + "-authors.txt -  authors info ")
            for author in tqdm(author_name_id_dict, total=len(author_name_id_dict)):
                open("../dblp-" + self.year + "/" + network + "-authors.txt", "a").write(
                    str(author_name_id_dict[author]) + "\t" + author + "\n")

    def write_titles_info(self, network):
        """
        This function reads a file ../dblp-year/dblp.txt
        extracts title of the publications, builds a dictionary, assigns unique id to each title.
        writes dictionary to a  file ../dblp-year/dblp-titles.txt
        :return:
        """
        import utilities
        if network == "db":
            titles_set = set()
            with open("../dblp-" + self.year + "/" + network + ".txt") as file:
                n_lines = utilities.get_num_lines("../dblp-" + self.year + "/" + network + ".txt")
                tqdm.write("processing ../dblp-" + self.year + "/" + network + ".txt - titles info ")
                for line in tqdm(file, total=n_lines):
                    if "<title>" in line:
                        title = line[line.index("<title>") + len("<title>"):line.index("</title>") - 1]
                        if title not in titles_set:
                            titles_set.add(title)
                        else:
                            pass
            title_id = 1
            title_id_name_dict = dict()
            tqdm.write("writing ../dblp-" + self.year + "/" + network + "-titles.txt -  titles info ")
            open("../dblp-" + self.year + "/" + network + "-titles.txt", "w").close()
            for title in tqdm(titles_set, total=len(titles_set)):
                title_id_name_dict[title_id] = title
                open("../dblp-" + self.year + "/" + network + "-titles.txt", "a").write(
                    str(title_id) + "\t" + title + "\n")
                title_id += 1
        else:
            dblp_title_name_id_dict = dict()
            with open("../dblp-" + self.year + "/db-titles.txt", "r") as file:
                for line in file:
                    words = line.strip("\n").split("\t")
                    dblp_title_name_id_dict[words[1]] = words[0]
            title_id_name_dict = dict()
            with open("../dblp-" + self.year + "/" + network + ".txt") as file:
                n_lines = utilities.get_num_lines("../dblp-" + self.year + "/" + network + ".txt")
                tqdm.write("processing ../dblp-" + self.year + "/" + network + ".txt - titles info ")
                for line in tqdm(file, total=n_lines):
                    if "<title>" in line:
                        title = line[line.index("<title>") + len("<title>"):line.index("</title>") - 1]
                        title_id_name_dict[dblp_title_name_id_dict[title]] = title
            tqdm.write("writing ../dblp-" + self.year + "/" + network + "-titles.txt -  titles info ")
            open("../dblp-" + self.year + "/" + network + "-titles.txt", "w").close()
            for title_id in tqdm(title_id_name_dict, total=len(title_id_name_dict)):
                open("../dblp-" + self.year + "/" + network + "-titles.txt", "a").write(
                    str(title_id) + "\t" + title_id_name_dict[title_id] + "\n")

    def write_skills_info(self, network):
        """
        This function reads a file ../dblp-year/dblp.txt
        extracts pairs of authors for each publication, builds a dictionary, author as key and
        list of their publications as value.
        non-trivial words that appear at least twice in author publications are considered as skills of that author
        non-trivial words are free from numbers, symbols and non dictionary(brown of nltk) words, stopwords of nltk
        writes collaborations dictionary to a  file ../dblp-year/dblp-author-pair-collaborations.txt
        author id pair as key and list of shared publication ids as value
        writes author skills dictionary to a  file ../dblp-year/dblp-author-skills.txt
        author id as key and list of skill ids as value
        writes author skills dictionary to a  file ../dblp-year/dblp-skills.txt
        skill id as key and skill title as value
        :return:
        """
        import utilities
        dblp_title_id_name_dict = dict()
        with open("../dblp-" + self.year + "/" + network + "-titles.txt", "r") as file:
            for line in file:
                words = line.strip("\n").split("\t")
                dblp_title_id_name_dict[words[0]] = words[1]
        dblp_author_name_id_dict = dict()
        with open("../dblp-" + self.year + "/" + network + "-authors.txt", "r") as file:
            for line in file:
                words = line.strip("\n").split("\t")
                dblp_author_name_id_dict[words[1]] = words[0]
        author_id_skill_ids_dict = dict()
        author_id_pubs_dict = dict()
        collaborations_dict = dict()
        with open("../dblp-" + self.year + "/" + network + ".txt") as file:
            n_lines = utilities.get_num_lines("../dblp-" + self.year + "/" + network + ".txt")
            open("../dblp-" + self.year + "/" + network + "-rec.txt", "w").close()
            tqdm.write("processing ../dblp-" + self.year + "/" + network + ".txt - skills info ")
            # for line in file:
            for line in tqdm(file, total=n_lines):
                year = ""
                if "<year>" in line:
                    year = line[line.index("<year>") + len("<year>"):line.index("</year>")]
                else:
                    pass
                title = ""
                if "<title>" in line:
                    title = line[line.index("<title>") + len("<title>"):line.index("</title>") - 1]
                else:
                    pass
                authors = list()
                if "<author>" in line:
                    authors = line[line.index("<author>") + len("<author>"):line.index("</author>")].split(":")
                    for author in authors:
                        title_key = utilities.get_key(dblp_title_id_name_dict, title)
                        if dblp_author_name_id_dict[author] in author_id_pubs_dict:
                            if title_key in author_id_pubs_dict[dblp_author_name_id_dict[author]]:
                                pass
                            else:
                                author_id_pubs_dict[dblp_author_name_id_dict[author]].append(title_key)
                        else:
                            author_id_pubs_dict[dblp_author_name_id_dict[author]] = list()
                            author_id_pubs_dict[dblp_author_name_id_dict[author]].append(title_key)
                    if len(authors) > 1:
                        for collaborator_1 in authors:
                            for collaborator_2 in authors:
                                if collaborator_1 != collaborator_2:
                                    if collaborator_1 in dblp_author_name_id_dict and \
                                            collaborator_2 in dblp_author_name_id_dict:
                                        title_key = utilities.get_key(dblp_title_id_name_dict, title)
                                        if str(dblp_author_name_id_dict[collaborator_1]) + ":" + str(
                                                dblp_author_name_id_dict[collaborator_2]) in collaborations_dict:
                                            if title_key is not None and title_key not in collaborations_dict[
                                                str(dblp_author_name_id_dict[collaborator_1]) + ":" + str(
                                                    dblp_author_name_id_dict[collaborator_2])]:
                                                collaborations_dict[
                                                    str(dblp_author_name_id_dict[collaborator_1]) + ":" + str(
                                                        dblp_author_name_id_dict[collaborator_2])].append(title_key)
                                            else:
                                                pass
                                        elif str(dblp_author_name_id_dict[collaborator_2]) + ":" + str(
                                                dblp_author_name_id_dict[collaborator_1]) in collaborations_dict:
                                            if title_key is not None and title_key not in collaborations_dict[
                                                str(dblp_author_name_id_dict[collaborator_2]) + ":" + str(
                                                    dblp_author_name_id_dict[collaborator_1])]:
                                                collaborations_dict[
                                                    str(dblp_author_name_id_dict[collaborator_2]) + ":" + str(
                                                        dblp_author_name_id_dict[collaborator_1])].append(title_key)
                                            else:
                                                pass
                                        elif title_key is not None:
                                            collaborations_dict[
                                                str(dblp_author_name_id_dict[collaborator_2]) + ":" + str(
                                                    dblp_author_name_id_dict[collaborator_1])] = list()
                                            collaborations_dict[
                                                str(dblp_author_name_id_dict[collaborator_2]) + ":" + str(
                                                    dblp_author_name_id_dict[collaborator_1])].append(title_key)
                                        else:
                                            pass
                                    else:
                                        pass
                else:
                    pass
                journal = ""
                if "<journal>" in line:
                    journal = line[line.index("<journal>") + len("<journal>"):line.index("</journal>")]
                else:
                    pass
                if "<booktitle>" in line:
                    journal = line[line.index("<booktitle>") + len("<booktitle>"):line.index("</booktitle>")]
                else:
                    pass
                if len(year) > 0 and int(year) > 1999 and len(authors) > 0 and len(title.split()) > 3 \
                        and len(journal) > 0:
                    record = year
                    record += "\t" + journal
                    record += "\t" + ":".join(authors)
                    record += "\t" + title + "\n"
                    open("../dblp-" + self.year + "/" + network + "-rec.txt", "a").write(record)
        tqdm.write("writing ../dblp-" + self.year + "/" + network + ".txt -  author collaborations info ")
        open("../dblp-" + self.year + "/" + network + "-author-pair-collaborations.txt", "w").close()
        for collab in tqdm(collaborations_dict, total=len(collaborations_dict)):
            open("../dblp-" + self.year + "/" + network + "-author-pair-collaborations.txt", "a").write(
                str(collab) + "\t" + ",".join(collaborations_dict[collab]) + "\n")
        tqdm.write("writing ../dblp-" + self.year + "/" + network + ".txt - writing author publications info ")
        open("../dblp-" + self.year + "/" + network + "-author-publications.txt", "w").close()
        for author in tqdm(author_id_pubs_dict, total=len(author_id_pubs_dict)):
            open("../dblp-" + self.year + "/" + network + "-author-publications.txt", "a").write(
                str(author) + "\t" + ",".join(author_id_pubs_dict[author]) + "\n")
        import os
        open("../dblp-" + self.year + "/" + network + "-records.txt", "w").close()
        os.system("sort ../dblp-" + self.year + "/" + network + "-rec.txt > ../dblp-"
                  + self.year + "/" + network + "-records.txt")
        os.system("rm -v ../dblp-" + self.year + "/" + network + "-rec.txt >> /dev/null")
        if network == "db":
            skill_set = set()
            author_id_skills_dict = dict()
            for author in tqdm(author_id_pubs_dict, total=len(author_id_pubs_dict)):
                pub_s = ""
                author_id_skills_dict[author] = list()
                for pub in author_id_pubs_dict[author]:
                    pub_s += " " + dblp_title_id_name_dict[pub]
                for skill in get_dblp_skills(pub_s):
                    skill_set.add(skill)
                    author_id_skills_dict[author].append(skill)
            skill_id = 1
            skill_id_name_dict = dict()
            skill_name_id_dict = dict()
            open("../dblp-" + self.year + "/" + network + "-skills.txt", "w").close()
            for skill in skill_set:
                skill_id_name_dict[skill_id] = skill
                skill_name_id_dict[skill] = skill_id
                open("../dblp-" + self.year + "/" + network + "-skills.txt", "a").write(
                    str(skill_id) + "\t" + skill + "\n")
                skill_id += 1
            tqdm.write("writing ../dblp-" + self.year + "/" + network + ".txt - writing author skills info ")
            open("../dblp-" + self.year + "/" + network + "-author-skills.txt", "w").close()
            for author in tqdm(author_id_skills_dict, total=len(author_id_skills_dict)):
                author_id_skill_ids_dict[author] = list()
                for skill in author_id_skills_dict[author]:
                    author_id_skill_ids_dict[author].append(skill_name_id_dict[skill])
                if len(author_id_skill_ids_dict[author]) > 0:
                    open("../dblp-" + self.year + "/" + network + "-author-skills.txt", "a").write(
                        str(author) + "\t" + ",".join([str(intg) for intg in author_id_skill_ids_dict[author]]) + "\n")
        else:
            dblp_skill_name_id_dict = dict()
            with open("../dblp-" + self.year + "/db-skills.txt", "r") as file:
                for line in file:
                    line_words = line.strip("\n").split()
                    dblp_skill_name_id_dict[line_words[1]] = line_words[0]
            author_id_skill_ids_dict = dict()
            for author in tqdm(author_id_pubs_dict, total=len(author_id_pubs_dict)):
                pub_s = ""
                author_id_skill_ids_dict[author] = list()
                for pub_id in author_id_pubs_dict[author]:
                    pub_s += " " + dblp_title_id_name_dict[pub_id]
                    all_skills = get_cmnt_skills(pub_s)
                    for skill in all_skills:
                        if skill in dblp_skill_name_id_dict:
                            author_id_skill_ids_dict[author].append(dblp_skill_name_id_dict[skill])
            for author_id in tqdm(author_id_skill_ids_dict, total=len(author_id_skill_ids_dict)):
                if len(author_id_skill_ids_dict[author_id]) > 0:
                    open("../dblp-" + self.year + "/" + network + "-author-skills.txt", "a").write(
                        str(author_id) + "\t" + ",".join([str(intg) for intg in
                                                          author_id_skill_ids_dict[author_id]]) + "\n")

    def build_graph(self, network):
        # import matplotlib.pyplot as plt
        # Read authors : nodes
        author_id_name_dict = dict()
        with open("../dblp-" + self.year + "/" + network + "-authors.txt", "r") as file:
            for line in file:
                line_words = line.strip("\n").split("\t")
                author_id_name_dict[line_words[0]] = line_words[1]
        # Read authors skills : node attributes
        author_id_skill_ids_dict = dict()
        with open("../dblp-" + self.year + "/" + network + "-author-skills.txt", "r") as file:
            for line in file:
                line_words = line.strip("\n").split("\t")
                author_id_skill_ids_dict[line_words[0]] = line_words[1]
        # Read author publications : to calculate jaccard distance
        author_id_pub_ids_dict = dict()
        with open("../dblp-" + self.year + "/" + network + "-author-publications.txt", "r") as file:
            for line in file:
                line_words = line.strip("\n").split("\t")
                author_id_pub_ids_dict[line_words[0]] = line_words[1]
        # Read collaborations
        collab_id_pub_ids_dict = dict()
        with open("../dblp-" + self.year + "/" + network + "-author-pair-collaborations.txt", "r") as file:
            for line in file:
                line_words = line.strip("\n").split("\t")
                collab_id_pub_ids_dict[line_words[0]] = line_words[1]
        import networkx as nx
        graph = nx.Graph()
        graph.name = network + " Network"
        for author_id in author_id_skill_ids_dict:
            if author_id in author_id_name_dict:
                graph.add_node(author_id, name=author_id_name_dict[author_id],
                               skills=author_id_skill_ids_dict[author_id])
        for collab in collab_id_pub_ids_dict:
            u = collab.split(":")[0]
            v = collab.split(":")[1]
            num = len(collab_id_pub_ids_dict[collab].split(","))
            den = len(author_id_pub_ids_dict[u].split(",")) + len(author_id_pub_ids_dict[v].split(",")) - num
            jd = round(num / den, 3)
            graph.add_edge(u, v, weight=jd)
        largest_cc = graph.subgraph(sorted(nx.connected_components(graph), key=len, reverse=True)[0])
        # largest_cc = graph.subgraph(max([cc for cc in nx.connected_components(graph)])).copy()
        nx.draw_circular(largest_cc, with_labels=True)
        nx.write_gml(largest_cc, "../dblp-" + self.year + "/" + network + ".gml")
        # plt.show()

    def generate_community_tasks(self, community, ntasks) -> None:
        """
        This method called once, generates community tasks 1700 and 17
        :return:
        """
        import glob
        import random
        import networkx as nx
        max_no = 0
        graph = nx.read_gml("../dblp-" + self.year + "/" + community + ".gml")
        community_skills = self.get_community_skills_set(graph)
        for _ in range(5):
            file_list = glob.glob("../dblp-" + self.year + "/" + community + "-" + str(ntasks) + "-*.txt")
            if len(file_list) >= 5:
                print("please delete existing(old) files")
                break
            elif len(file_list) > 0:
                max_no = len(file_list)
                file_path = "../dblp-" + self.year + "/" + community + "-" + str(ntasks) + "-tasks-" \
                            + str(max_no) + ".txt"
            else:
                file_path = "../dblp-" + self.year + "/" + community + "-" + str(ntasks) + "-tasks-" \
                            + str(max_no) + ".txt"
            all_tasks = list()
            open(file_path, "w").close()
            if ntasks == 17:
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

    @staticmethod
    def get_community_skills_set(graph) -> set:
        """
        skill set of community is returned
        :param graph:
        :return set:
        """
        community_skills = set()
        for node in graph.nodes():
            if len(graph.nodes[node]) > 0:
                for skill in graph.nodes[node]["skills"].split(","):
                    if skill is not None and len(skill) > 0:
                        community_skills.add(skill)
        return community_skills

    def get_task_from_title_graph(self, graph, publication) -> list:
        """
        returns non trivial words of publication as skills packed in set
        used to get skills of an expert
        non trivial keywords that appear at least twice in his/her publications are skills
        :param graph:
        :param publication:
        :return:
        """
        from nltk import word_tokenize
        import re
        all_words = word_tokenize(re.sub(r'[^a-zA-Z]', ' ', publication))
        task_skills = set()
        graph_skills = set()
        skill_name_id_dict = dict()
        with open("../dblp-" + self.year + "/dblp-skills.txt", "r") as file:
            for line in file:
                line_words = line.strip("\n").split("\t")
                skill_name_id_dict[line_words[1]] = line_words[0]
        for node in graph.nodes():
            if len(graph.nodes[node]) >= 2:
                for skill in graph.nodes[node]["skills"].split(","):
                    graph_skills.add(skill)
        for word in all_words:
            if word.lower() in skill_name_id_dict:
                task_skills.add(skill_name_id_dict[word.lower()])
        lst = list(task_skills.intersection(graph_skills))
        return sorted(lst)


def multiprocessing_func(l_txt):
    nyear = "2015"
    dblp_dt = DBLP_Data(nyear)
    # dblp_dt.write_authors_info(l_txt)
    # dblp_dt.write_titles_info(l_txt)
    # dblp_dt.write_skills_info(l_txt)
    dblp_dt.build_graph(l_txt)
    dblp_dt.generate_community_tasks(l_txt, 17)


if __name__ == '__main__':
    start_time = time.time()
    myear = "2015"
    mnetwork = "db"
    dblp_data = DBLP_Data(myear)
    # dblp_data.write_authors_info(mnetwork)
    # dblp_data.write_titles_info(mnetwork)
    # dblp_data.write_skills_info(mnetwork)
    dblp_data.build_graph(mnetwork)
    dblp_data.generate_community_tasks(mnetwork, 17)
    processes = []
    for txt in ["vldb", "sigmod", "icde", "icdt", "edbt", "pods"]:
        # for txt in ["pods"]:
        p = multiprocessing.Process(target=multiprocessing_func, args=(txt,))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()
    tqdm.write('Time taken = {} seconds'.format(time.time() - start_time))
