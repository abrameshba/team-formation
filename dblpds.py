import time

from tqdm import tqdm


class DBLPData:

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
        if network == "dblp":
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
        if network == "dblp":
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
        import utilities
        if network == "dblp":
            skill_set = set()
            author_id_skills_dict = dict()
            for author in tqdm(author_id_pubs_dict, total=len(author_id_pubs_dict)):
                pub_s = ""
                author_id_skills_dict[author] = list()
                for pub in author_id_pubs_dict[author]:
                    pub_s += " " + dblp_title_id_name_dict[pub]
                for skill in utilities.get_dblp_skills_from_pub(pub_s):
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
                    all_skills = utilities.get_dblp_skills_from_pub(pub_s)
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
            graph.add_edge(u, v, cc=jd)
        largest_cc = graph.subgraph(sorted(nx.connected_components(graph), key=len, reverse=True)[0])
        adict = dict()
        for cc in sorted(nx.connected_components(graph)):
            if len(cc) in adict:
                adict[len(cc)] += 1
            else:
                adict[len(cc)] = 1
        with open("../dblp-" + self.year + "/" + network + ".cc", "w") as file:
            for key in adict:
                file.write("{}\t{}\n".format(key, adict[key]))
        # largest_cc = graph.subgraph(max([cc for cc in nx.connected_components(graph)])).copy()
        nx.draw_circular(largest_cc, with_labels=True)
        nx.write_gml(largest_cc, "../dblp-" + self.year + "/" + network + ".gml")
        # plt.show()

    def alpha_diversity(self, network):
        """
        returns Shannon entropy
        :return:
        """
        import math
        # for network in ["icdt", "pods", "edbt", "vldb", "icde", "sigmod", "db"]:
        graph = nx.read_gml("../dblp-" + self.year + "/" + network + ".gml")
        open("../dblp-" + self.year + "/" + network + "-author-alpha.txt", "w").close()
        for node in graph.nodes:
            if len(graph.nodes[node]) > 0:
                skl_count = graph.nodes[node]["skills"].split(",")
                simpson_d = 1 / len(skl_count)
                simpson_inv = 1 / simpson_d
                gini_simpson_div = 1 - simpson_d
                shannon_alpha = math.log(len(skl_count))
                record = str(node)
                record += "\t" + str(graph.nodes[node]["name"])
                record += "\t" + str(round(shannon_alpha, 3))
                record += "\t" + str(round(simpson_inv, 3))
                record += "\t" + str(round(gini_simpson_div, 3)) + "\n"
                open("../dblp-" + self.year + "/" + network + "-author-alpha.txt", "a").write(record)

    def generate_random_tasks(self, network, ntasks) -> None:
        """
        This method called once, generates network tasks 1700 and 17
        :return:
        """
        import glob
        import random
        import networkx as nx
        import utilities
        max_no = 0
        graph = nx.read_gml("../dblp-" + self.year + "/" + network + ".gml")
        network_skills = set()
        skill_experts = utilities.get_skill_experts_dict(graph)
        rare_skills = set()
        for skill in skill_experts:
            if len(skill_experts[skill]) <= 3:
                rare_skills.add(skill)  # rare skills
            else:
                network_skills.add(skill)
        for _ in range(3):
            file_list = glob.glob("../dblp-" + self.year + "/" + network + "-" + str(ntasks) + "-*.txt")
            if len(file_list) >= 3:
                print("please delete existing(old) files")
                break
            elif len(file_list) > 0:
                max_no = len(file_list)
                file_path = "../dblp-" + self.year + "/" + network + "-" + str(ntasks) + "-" \
                            + str(max_no) + ".txt"
            else:
                file_path = "../dblp-" + self.year + "/" + network + "-" + str(ntasks) + "-" \
                            + str(max_no) + ".txt"
            all_tasks = list()
            open(file_path, "w").close()
            iters = int(ntasks / 17)
            for skills_count in range(4, 21):
                for iter_count in range(iters):
                    task = set()
                    while len(task) < skills_count:
                        task.add(random.choice(list(network_skills)))
                        if len(task) == skills_count:
                            all_tasks.append(list(task))
                    for task in all_tasks:
                        for skill in task:
                            open(file_path, "a").write(skill + "\t")
                        open(file_path, "a").write("\n")
                    all_tasks.clear()

    @staticmethod
    def get_network_skills_set(graph) -> set:
        """
        skill set of network is returned
        :param graph:
        :return set:
        """
        network_skills = set()
        for node in graph.nodes():
            if len(graph.nodes[node]) > 0:
                for skill in graph.nodes[node]["skills"].split(","):
                    if skill is not None and len(skill) > 0:
                        network_skills.add(skill)
        return network_skills

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

    def analysis(self, network):
        """
        skills covered by 2 hop neighbourhood of high collaborating nodes is 1.0
        :return:
        """
        import utilities
        import networkx as nx
        # dblp_dt = DBLP_Data(myear)
        # for txt in ["vldb", "sigmod", "icde", "icdt", "edbt", "pods", "www", "kdd", "sdm", "pkdd", "icdm", "icml",
        #             "ecml", "colt", "uai", "soda", "focs", "stoc", "stacs", "db", "dm", "ai", "th"]:
        l_graph = nx.read_gml("../dblp-" + self.year + "/" + network + ".gml")
        avg_degree = (2 * l_graph.number_of_edges()) / float(l_graph.number_of_nodes())
        print(network)
        cs = self.get_network_skills_set(l_graph)
        for gama in [1, 2, 3]:
            hc = sorted([n for n, d in l_graph.degree() if len(l_graph.nodes[n]) > 0 and
                         d >= gama * avg_degree], reverse=True)
            print("lambda : "+str(gama)+" : " + str(round(len(hc) / l_graph.number_of_nodes(),3)))
            for hops in [1, 2, 3]:
                hcn = set()
                for n in hc:
                    hcn.update(utilities.within_k_nbrs(l_graph, n, hops))
                hcs = self.get_network_skills_set(l_graph.subgraph(hcn).copy())
                print("% of nodes  : " + str(hops) + " : " + str(round(len(hcn) / l_graph.number_of_nodes(),3)), end="\t")
                print("% of skills  : " + str(round(len(hcs) / len(cs),3)))

    def write_statistics(self, network):
        """
        write technical statistics to network_tech_stats.txt
        :return:
        """
        import collections
        import math
        import networkx as nx
        graph = nx.read_gml("../dblp-" + self.year + "/" + network + ".gml")
        degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)  # degree sequence
        # print "Degree sequence", degree_sequence
        avg_degree = (2 * graph.number_of_edges()) / float(graph.number_of_nodes())
        degree_count = collections.Counter(degree_sequence)
        hcn = 0
        with open("../dblp-" + self.year + "/" + network + "-hc.txt", "w") as hc, \
                open("../dblp-" + self.year + "/" + network + "-lc.txt", "w") as lc:
            for tpl in degree_count.items():
                if tpl[0] >= 2 * avg_degree:
                    hc.write("{}\t{}\t{:.2f}\n".format(tpl[0], tpl[1], math.log10(tpl[1])))
                    hcn += tpl[1]
                elif tpl[0] > 0:
                    lc.write("{}\t{}\t{:.2f}\n".format(tpl[0], tpl[1], math.log10(tpl[1])))
                else:
                    pass
        import utilities
        skill_experts = utilities.get_skill_experts_dict(graph)
        skill_freq = dict()
        total_experts = 0
        for skill in skill_experts:
            if len(skill_experts[skill]) in skill_freq:  # skill with same number of experts
                skill_freq[len(skill_experts[skill])] += 1
            else:
                skill_freq[len(skill_experts[skill])] = 1
            total_experts += len(skill_experts[skill])  # expert counted as many times as skills
        # number of experts per skill and number of such skills
        with open("../dblp-" + self.year + "/" + network + "-experts-per-skill.txt", "w") as file:
            for experts_freq in skill_freq:
                file.write("{}\t{}\n".format(experts_freq, skill_freq[experts_freq]))
        experts = dict()
        total_skills = 0
        for node in graph.nodes:
            if len(graph.nodes[node]) > 1:
                skl_count = len(graph.nodes[node]["skills"].split(","))
                if skl_count in experts:
                    experts[skl_count] += 1
                else:
                    experts[skl_count] = 1
                total_skills += skl_count  # skill is counted as many times as possessed by experts
        # number of skills of an expert and number experts with given number of skills
        with open("../dblp-" + self.year + "/" + network + "-skills-per-expert.txt", "w") as file1:
            for skl_count in experts:
                file1.write("{}\t{}\n".format(skl_count, experts[skl_count]))
        skills_per_expert = round(total_skills / nx.number_of_nodes(graph), 2)
        experts_per_skill = round(total_experts / len(skill_experts), 2)
        record = network
        record += "\t" + str(graph.number_of_nodes())
        record += "\t" + str(graph.number_of_edges())
        record += "\t" + str(len(skill_experts))
        record += "\t" + str(experts_per_skill)  # experts per skill
        record += "\t" + str(skills_per_expert)  # skills per expert
        # ratio of high collab nodes to total_experts nodes
        record += "\t" + str(round(hcn / graph.number_of_nodes(), 2))
        record += "\t" + str(nx.diameter(graph))
        record += "\t" + str(round(nx.average_shortest_path_length(graph), 2))
        open("../dblp-" + myear + "/stats-summary-now.txt", "a").write(record + "\n")

    def generate_distributed_tasks(self, network):
        import networkx as nx
        import utilities
        graph = nx.read_gml("../dblp-" + self.year + "/" + network + ".gml")
        skill_freq = dict()
        total = 0
        skill_experts = utilities.get_skill_experts_dict(graph)
        for skill in skill_experts:
            if len(skill_experts[skill]) in skill_freq:  # skill with same number of experts
                skill_freq[len(skill_experts[skill])] += 1
            else:
                skill_freq[len(skill_experts[skill])] = 1
            total += len(skill_experts[skill])
        # skill_experts = utilities.get_skill_experts_dict(graph)
        experts_per_skill = round(total / len(skill_experts), 2)
        popular_skills = set()
        unusual_skills = set()
        rare_skills = set()
        for skill in skill_experts:
            if len(skill_experts[skill]) >= experts_per_skill:
                popular_skills.add(skill)
            else:
                if len(skill_experts[skill]) <= 3:
                    rare_skills.add(skill)
                else:
                    unusual_skills.add(skill)  # rare skills
        rec = ""
        rec += str(len(popular_skills)) + "\t"
        rec += str(len(unusual_skills)) + "\t"
        rec += str(len(rare_skills)) + "\t"
        print(network + "\t" + rec + "\n")
        for tot_skl in [10, 15, 20]:
            usual_skills_list = list(popular_skills)
            unusual_skills_list = list(unusual_skills)
            import random
            import glob
            for _ in range(3):
                file_list = glob.glob("../dblp-" + self.year + "/" + network + "-" + str(tot_skl) + "-*.txt")
                if len(file_list) >= 3:
                    print("please delete existing(old) files")
                    break
                else:
                    max_no = len(file_list)
                    file_path = "../dblp-" + self.year + "/" + network + "-" + str(tot_skl) + "-" + str(
                        max_no) + ".txt"
                open(file_path, "w").close()
                if len(popular_skills) < tot_skl:
                    print("short of common skills : " + network)
                    return
                for i in range(tot_skl):
                    tasks = []
                    for run in range(10):
                        task = set()
                        for k in range(i):
                            while len(task) < tot_skl:
                                task.add(random.choice(unusual_skills_list))
                        for j in range(tot_skl):
                            while len(task) <= j <= len(popular_skills):
                                task.add(random.choice(usual_skills_list))
                        tasks.append(task)
                    for task in tasks:
                        for skill in task:
                            open(file_path, "a").write(skill + "\t")
                        open(file_path, "a").write("\n")


class BIBSNMData:

    def __init__(self, year):
        self.year = year

    def write_authors_info(self, network):
        import utilities
        if network == "bbsnm":
            authors_name_set = set()
            with open("../bbsnm-" + self.year + "/" + network + ".txt") as file:
                n_lines = utilities.get_num_lines("../bbsnm-" + self.year + "/" + network + ".txt")
                tqdm.write("processing ../bbsnm-" + self.year + "/" + network + ".txt - authors info ")
                for line in tqdm(file, total=n_lines):
                    wrds = line.strip("\n").split("\t")
                    if len(wrds) == 4:
                        authors = wrds[2].split(" and ")
                        for author in authors:
                            if len(author) > 1 and author not in authors_name_set:
                                authors_name_set.add(author.strip(" "))
                            else:
                                pass
            author_id = 1
            author_id_name_dict = dict()
            author_name_id_dict = dict()
            open("../bbsnm-" + self.year + "/" + network + "-authors.txt", "w").close()
            tqdm.write("writing ../bbsnm-" + self.year + "/" + network + "-authors.txt -  authors info ")
            for author in tqdm(authors_name_set, total=len(authors_name_set)):
                author_id_name_dict[author_id] = author
                author_name_id_dict[author] = author_id
                open("../bbsnm-" + self.year + "/" + network + "-authors.txt", "a").write(
                    str(author_id) + "\t" + author + "\n")
                author_id += 1
        else:
            dblp_author_name_id_dict = dict()
            with open("../bbsnm-" + self.year + "/bbsnm-authors.txt", "r") as file:
                for line in file:
                    words = line.strip("\n").split("\t")
                    dblp_author_name_id_dict[words[1]] = words[0]
            author_name_id_dict = dict()
            with open("../bbsnm-" + self.year + "/" + network + ".txt") as file:
                n_lines = utilities.get_num_lines("../bbsnm-" + self.year + "/" + network + ".txt")
                tqdm.write("processing ../bbsnm-" + self.year + "/" + network + ".txt - authors info ")
                for line in tqdm(file, total=n_lines):
                    wrds = line.strip("\n").split("\t")
                    authors = wrds[2].split(" and ")
                    for author in authors:
                        if author not in author_name_id_dict:
                            author_name_id_dict[author] = dblp_author_name_id_dict[author]
            open("../bbsnm-" + self.year + "/" + network + "-authors.txt", "w").close()
            tqdm.write("writing ../bbsnm-" + self.year + "/" + network + "-authors.txt -  authors info ")
            for author in tqdm(author_name_id_dict, total=len(author_name_id_dict)):
                open("../bbsnm-" + self.year + "/" + network + "-authors.txt", "a").write(
                    str(author_name_id_dict[author]) + "\t" + author + "\n")

    def write_titles_info(self, network):
        """
        This function reads a file ../bbsnm-year/bbsnm.txt
        extracts title of the publications, builds a dictionary, assigns unique id to each title.
        writes dictionary to a  file ../bbsnm-year/bbsnm-titles.txt
        :return:
        """
        import utilities
        if network == "bbsnm":
            titles_set = set()
            with open("../bbsnm-" + self.year + "/" + network + ".txt") as file:
                n_lines = utilities.get_num_lines("../bbsnm-" + self.year + "/" + network + ".txt")
                tqdm.write("processing ../bbsnm-" + self.year + "/" + network + ".txt - titles info ")
                for line in tqdm(file, total=n_lines):
                    wrds = line.strip("\n").split("\t")
                    if len(wrds) == 4:
                        title = wrds[3]
                        if title not in titles_set:
                            titles_set.add(title)
                        else:
                            pass
            title_id = 1
            title_id_name_dict = dict()
            tqdm.write("writing ../bbsnm-" + self.year + "/" + network + "-titles.txt -  titles info ")
            open("../bbsnm-" + self.year + "/" + network + "-titles.txt", "wdblp").close()
            for title in tqdm(titles_set, total=len(titles_set)):
                title_id_name_dict[title_id] = title
                open("../bbsnm-" + self.year + "/" + network + "-titles.txt", "a").write(
                    str(title_id) + "\t" + title + "\n")
                title_id += 1
        else:
            dblp_title_name_id_dict = dict()
            with open("../bbsnm-" + self.year + "/bbsnm-titles.txt", "r") as file:
                for line in file:
                    words = line.strip("\n").split("\t")
                    dblp_title_name_id_dict[words[1]] = words[0]
            title_id_name_dict = dict()
            with open("../bbsnm-" + self.year + "/" + network + ".txt") as file:
                n_lines = utilities.get_num_lines("../bbsnm-" + self.year + "/" + network + ".txt")
                tqdm.write("processing ../bbsnm-" + self.year + "/" + network + ".txt - titles info ")
                for line in tqdm(file, total=n_lines):
                    if "<title>" in line:
                        title = line[line.index("<title>") + len("<title>"):line.index("</title>") - 1]
                        title_id_name_dict[dblp_title_name_id_dict[title]] = title
            tqdm.write("writing ../bbsnm-" + self.year + "/" + network + "-titles.txt -  titles info ")
            open("../bbsnm-" + self.year + "/" + network + "-titles.txt", "w").close()
            for title_id in tqdm(title_id_name_dict, total=len(title_id_name_dict)):
                open("../bbsnm-" + self.year + "/" + network + "-titles.txt", "a").write(
                    str(title_id) + "\t" + title_id_name_dict[title_id] + "\n")

    def write_skills_info(self, network):
        """
        This function reads a file ../bbsnm-year/dblp.txt
        extracts pairs of authors for each publication, builds a dictionary, author as key and
        list of their publications as value.
        non-trivial words that appear at least twice in author publications are considered as skills of that author
        non-trivial words are free from numbers, symbols and non dictionary(brown of nltk) words, stopwords of nltk
        writes collaborations dictionary to a  file ../bbsnm-year/dblp-author-pair-collaborations.txt
        author id pair as key and list of shared publication ids as value
        writes author skills dictionary to a  file ../bbsnm-year/dblp-author-skills.txt
        author id as key and list of skill ids as value
        writes author skills dictionary to a  file ../bbsnm-year/dblp-skills.txt
        skill id as key and skill title as value
        :return:
        """
        import utilities
        dblp_title_id_name_dict = dict()
        with open("../bbsnm-" + self.year + "/" + network + "-titles.txt", "r") as file:
            for line in file:
                words = line.strip("\n").split("\t")
                dblp_title_id_name_dict[words[0]] = words[1]
        dblp_author_name_id_dict = dict()
        with open("../bbsnm-" + self.year + "/" + network + "-authors.txt", "r") as file:
            for line in file:
                words = line.strip("\n").split("\t")
                dblp_author_name_id_dict[words[1]] = words[0]
        author_id_skill_ids_dict = dict()
        author_id_pubs_dict = dict()
        collaborations_dict = dict()
        with open("../bbsnm-" + self.year + "/" + network + ".txt") as file:
            n_lines = utilities.get_num_lines("../bbsnm-" + self.year + "/" + network + ".txt")
            open("../bbsnm-" + self.year + "/" + network + "-rec.txt", "w").close()
            tqdm.write("processing ../bbsnm-" + self.year + "/" + network + ".txt - skills info ")
            # for line in file:
            for line in tqdm(file, total=n_lines):
                wrds = line.strip("\n").split("\t")
                if len(wrds) == 4:
                    year = wrds[1]
                    journal = wrds[0]
                    title = wrds[3]
                    authors = wrds[2].split(" and ")
                    for authr in authors:
                        author = authr.strip(" ")
                        if author == '' or len(author) < 2:
                            continue
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
                    if len(year) > 0 and int(year) > 1999 and len(authors) > 0 and len(title.split()) > 3 \
                            and len(journal) > 0:
                        record = year
                        record += "\t" + journal
                        record += "\t" + ":".join(authors)
                        record += "\t" + title + "\n"
                        open("../bbsnm-" + self.year + "/" + network + "-rec.txt", "a").write(record)
        tqdm.write("writing ../bbsnm-" + self.year + "/" + network + ".txt -  author collaborations info ")
        open("../bbsnm-" + self.year + "/" + network + "-author-pair-collaborations.txt", "w").close()
        for collab in tqdm(collaborations_dict, total=len(collaborations_dict)):
            open("../bbsnm-" + self.year + "/" + network + "-author-pair-collaborations.txt", "a").write(
                str(collab) + "\t" + ",".join(collaborations_dict[collab]) + "\n")
        tqdm.write("writing ../bbsnm-" + self.year + "/" + network + ".txt - writing author publications info ")
        open("../bbsnm-" + self.year + "/" + network + "-author-publications.txt", "w").close()
        for author in tqdm(author_id_pubs_dict, total=len(author_id_pubs_dict)):
            open("../bbsnm-" + self.year + "/" + network + "-author-publications.txt", "a").write(
                str(author) + "\t" + ",".join(author_id_pubs_dict[author]) + "\n")
        import os
        open("../bbsnm-" + self.year + "/" + network + "-records.txt", "w").close()
        os.system("sort ../bbsnm-" + self.year + "/" + network + "-rec.txt > ../bbsnm-"
                  + self.year + "/" + network + "-records.txt")
        os.system("rm -v ../bbsnm-" + self.year + "/" + network + "-rec.txt >> /dev/null")
        import utilities
        if network == "bbsnm":
            skill_set = set()
            author_id_skills_dict = dict()
            for author in tqdm(author_id_pubs_dict, total=len(author_id_pubs_dict)):
                pub_s = ""
                author_id_skills_dict[author] = list()
                for pub in author_id_pubs_dict[author]:
                    pub_s += " " + dblp_title_id_name_dict[pub]
                for skill in utilities.get_dblp_skills_from_pub(pub_s):
                    skill_set.add(skill)
                    author_id_skills_dict[author].append(skill)
            skill_id = 1
            skill_id_name_dict = dict()
            skill_name_id_dict = dict()
            open("../bbsnm-" + self.year + "/" + network + "-skills.txt", "w").close()
            for skill in skill_set:
                skill_id_name_dict[skill_id] = skill
                skill_name_id_dict[skill] = skill_id
                open("../bbsnm-" + self.year + "/" + network + "-skills.txt", "a").write(
                    str(skill_id) + "\t" + skill + "\n")
                skill_id += 1
            tqdm.write("writing ../bbsnm-" + self.year + "/" + network + ".txt - writing author skills info ")
            open("../bbsnm-" + self.year + "/" + network + "-author-skills.txt", "w").close()
            for author in tqdm(author_id_skills_dict, total=len(author_id_skills_dict)):
                author_id_skill_ids_dict[author] = list()
                for skill in author_id_skills_dict[author]:
                    author_id_skill_ids_dict[author].append(skill_name_id_dict[skill])
                if len(author_id_skill_ids_dict[author]) > 0:
                    open("../bbsnm-" + self.year + "/" + network + "-author-skills.txt", "a").write(
                        str(author) + "\t" + ",".join([str(intg) for intg in author_id_skill_ids_dict[author]]) + "\n")
        else:
            dblp_skill_name_id_dict = dict()
            with open("../bbsnm-" + self.year + "/db-skills.txt", "r") as file:
                for line in file:
                    line_words = line.strip("\n").split()
                    dblp_skill_name_id_dict[line_words[1]] = line_words[0]
            author_id_skill_ids_dict = dict()
            for author in tqdm(author_id_pubs_dict, total=len(author_id_pubs_dict)):
                pub_s = ""
                author_id_skill_ids_dict[author] = list()
                for pub_id in author_id_pubs_dict[author]:
                    pub_s += " " + dblp_title_id_name_dict[pub_id]
                    all_skills = utilities.get_dblp_skills_from_pub(pub_s)
                    for skill in all_skills:
                        if skill in dblp_skill_name_id_dict:
                            author_id_skill_ids_dict[author].append(dblp_skill_name_id_dict[skill])
            for author_id in tqdm(author_id_skill_ids_dict, total=len(author_id_skill_ids_dict)):
                if len(author_id_skill_ids_dict[author_id]) > 0:
                    open("../bbsnm-" + self.year + "/" + network + "-author-skills.txt", "a").write(
                        str(author_id) + "\t" + ",".join([str(intg) for intg in
                                                          author_id_skill_ids_dict[author_id]]) + "\n")

    def build_graph(self, network):
        import matplotlib.pyplot as plt
        # Read authors : nodes
        author_id_name_dict = dict()
        with open("../bbsnm-" + self.year + "/" + network + "-authors.txt", "r") as file:
            for line in file:
                line_words = line.strip("\n").split("\t")
                author_id_name_dict[line_words[0]] = line_words[1]
        # Read authors skills : node attributes
        author_id_skill_ids_dict = dict()
        with open("../bbsnm-" + self.year + "/" + network + "-author-skills.txt", "r") as file:
            for line in file:
                line_words = line.strip("\n").split("\t")
                author_id_skill_ids_dict[line_words[0]] = line_words[1]
        # Read author publications : to calculate jaccard distance
        author_id_pub_ids_dict = dict()
        with open("../bbsnm-" + self.year + "/" + network + "-author-publications.txt", "r") as file:
            for line in file:
                line_words = line.strip("\n").split("\t")
                author_id_pub_ids_dict[line_words[0]] = line_words[1]
        # Read collaborations
        collab_id_pub_ids_dict = dict()
        with open("../bbsnm-" + self.year + "/" + network + "-author-pair-collaborations.txt", "r") as file:
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
            graph.add_edge(u, v, cc=jd)
        largest_cc = graph.subgraph(sorted(nx.connected_components(graph), key=len, reverse=True)[0])
        adict = dict()
        for cc in sorted(nx.connected_components(graph)):
            if len(cc) in adict:
                adict[len(cc)] += 1
            else:
                adict[len(cc)] = 1
        with open("../bbsnm-" + self.year + "/" + network + ".cc", "w") as file:
            for key in adict:
                file.write("{}\t{}\n".format(key, adict[key]))
        # largest_cc = graph.subgraph(max([cc for cc in nx.connected_components(graph)])).copy()
        nx.draw_circular(largest_cc, with_labels=True)
        nx.write_gml(largest_cc, "../bbsnm-" + self.year + "/" + network + ".gml")
        plt.show()

    def alpha_diversity(self, network):
        """
        returns Shannon entropy
        :return:
        """
        import math
        # for network in ["icdt", "pods", "edbt", "vldb", "icde", "sigmod", "db"]:
        graph = nx.read_gml("../bbsnm-" + self.year + "/" + network + ".gml")
        open("../bbsnm-" + self.year + "/" + network + "-author-alpha.txt", "w").close()
        for node in graph.nodes:
            if len(graph.nodes[node]) > 0:
                skl_count = graph.nodes[node]["skills"].split(",")
                simpson_d = 1 / len(skl_count)
                simpson_inv = 1 / simpson_d
                gini_simpson_div = 1 - simpson_d
                shannon_alpha = math.log(len(skl_count))
                record = str(node)
                record += "\t" + str(graph.nodes[node]["name"])
                record += "\t" + str(round(shannon_alpha, 3))
                record += "\t" + str(round(simpson_inv, 3))
                record += "\t" + str(round(gini_simpson_div, 3)) + "\n"
                open("../bbsnm-" + self.year + "/" + network + "-author-alpha.txt", "a").write(record)

    def generate_network_tasks(self, network, ntasks) -> None:
        """
        This method called once, generates network tasks 1700 and 17
        :return:
        """
        import glob
        import random
        import networkx as nx
        import utilities
        max_no = 0
        graph = nx.read_gml("../bbsnm-" + self.year + "/" + network + ".gml")
        network_skills = set()
        skill_experts = utilities.get_skill_experts_dict(graph)
        rare_skills = set()
        for skill in skill_experts:
            if len(skill_experts[skill]) <= 3:
                rare_skills.add(skill)
            else:
                network_skills.add(skill)  # rare skills
        for _ in range(3):
            file_list = glob.glob("../bbsnm-" + self.year + "/" + network + "-" + str(ntasks) + "-*.txt")
            if len(file_list) >= 3:
                print("please delete existing(old) files")
                break
            elif len(file_list) > 0:
                max_no = len(file_list)
                file_path = "../bbsnm-" + self.year + "/" + network + "-" + str(ntasks) + "-" \
                            + str(max_no) + ".txt"
            else:
                file_path = "../bbsnm-" + self.year + "/" + network + "-" + str(ntasks) + "-" \
                            + str(max_no) + ".txt"
            all_tasks = list()
            open(file_path, "w").close()
            iters = int(ntasks / 17)
            for skills_count in range(4, 21):
                for iter_count in range(iters):
                    task = set()
                    while len(task) < skills_count:
                        task.add(random.choice(list(network_skills)))
                        if len(task) == skills_count:
                            all_tasks.append(list(task))
                    for task in all_tasks:
                        for skill in task:
                            open(file_path, "a").write(skill + "\t")
                        open(file_path, "a").write("\n")
                    all_tasks.clear()

    @staticmethod
    def get_network_skills_set(graph) -> set:
        """
        skill set of network is returned
        :param graph:
        :return set:
        """
        network_skills = set()
        for node in graph.nodes():
            if len(graph.nodes[node]) > 0:
                for skill in graph.nodes[node]["skills"].split(","):
                    if skill is not None and len(skill) > 0:
                        network_skills.add(skill)
        return network_skills

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
        with open("../bbsnm-" + self.year + "/db-skills.txt", "r") as file:
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

    def analysis(self, network):
        """
        skills covered by 2 hop neighbourhood of high collaborating nodes is 1.0
        :return:
        """
        import utilities
        import networkx as nx
        # dblp_dt = DBLP_Data(myear)
        # for txt in ["vldb", "sigmod", "icde", "icdt", "edbt", "pods", "www", "kdd", "sdm", "pkdd", "icdm", "icml",
        #             "ecml", "colt", "uai", "soda", "focs", "stoc", "stacs", "db", "dm", "ai", "th"]:
        l_graph = nx.read_gml("../bbsnm-" + self.year + "/" + network + ".gml")
        avg_degree = (2 * l_graph.number_of_edges()) / float(l_graph.number_of_nodes())
        hc = sorted([n for n, d in l_graph.degree() if len(l_graph.nodes[n]) > 0 and
                     d >= 2 * avg_degree], reverse=True)
        hcn = set()
        for n in hc:
            hcn.update(utilities.within_k_nbrs(l_graph, n, 2))
        hcs = self.get_network_skills_set(l_graph.subgraph(hcn).copy())
        cs = self.get_network_skills_set(l_graph)
        print("skill coverage : " + str(len(hcs) / len(cs)))

    def write_statistics(self, network):
        """
        write technical statistics to network_tech_stats.txt
        :return:
        """
        import collections
        import math
        import networkx as nx
        graph = nx.read_gml("../bbsnm-" + self.year + "/" + network + ".gml")
        degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)  # degree sequence
        # print "Degree sequence", degree_sequence
        avg_degree = (2 * graph.number_of_edges()) / float(graph.number_of_nodes())
        degree_count = collections.Counter(degree_sequence)
        hcn = 0
        with open("../bbsnm-" + self.year + "/" + network + "-hc.txt", "w") as hc, \
                open("../bbsnm-" + self.year + "/" + network + "-lc.txt", "w") as lc:
            for tpl in degree_count.items():
                if tpl[0] >= 2 * avg_degree:
                    hc.write("{}\t{}\t{:.2f}\n".format(tpl[0], tpl[1], math.log10(tpl[1])))
                    hcn += tpl[1]
                elif tpl[0] > 0:
                    lc.write("{}\t{}\t{:.2f}\n".format(tpl[0], tpl[1], math.log10(tpl[1])))
                else:
                    pass
        import utilities
        skill_experts = utilities.get_skill_experts_dict(graph)
        skill_freq = dict()
        total_experts = 0
        for skill in skill_experts:
            if len(skill_experts[skill]) in skill_freq:  # skill with same number of experts
                skill_freq[len(skill_experts[skill])] += 1
            else:
                skill_freq[len(skill_experts[skill])] = 1
            total_experts += len(skill_experts[skill])  # expert counted as many times as skills
        # number of experts for a skill and number of such skills
        with open("../bbsnm-" + self.year + "/" + network + "-experts-per-skill.txt", "w") as file:
            for experts_freq in skill_freq:
                file.write("{}\t{}\n".format(experts_freq, skill_freq[experts_freq]))
        experts = dict()
        total_skills = 0
        for node in graph.nodes:
            if len(graph.nodes[node]) > 1:
                skl_count = len(graph.nodes[node]["skills"].split(","))
                if skl_count in experts:
                    experts[skl_count] += 1
                else:
                    experts[skl_count] = 1
                total_skills += skl_count  # skill is counted as many times as possessed by experts
        # number of skills of an expert and number experts with given number of skills
        with open("../bbsnm-" + self.year + "/" + network + "-skills-per-expert.txt", "w") as file1:
            for skl_count in experts:
                file1.write("{}\t{}\n".format(skl_count, experts[skl_count]))
        skills_per_expert = round(total_skills / nx.number_of_nodes(graph), 2)
        experts_per_skill = round(total_experts / len(skill_experts), 2)
        record = network
        record += "\t" + str(graph.number_of_nodes())
        record += "\t" + str(graph.number_of_edges())
        record += "\t" + str(len(skill_experts))
        record += "\t" + str(experts_per_skill)  # experts per skill
        record += "\t" + str(skills_per_expert)  # skills per expert
        # ratio of high collab nodes to total_experts nodes
        record += "\t" + str(round(hcn / graph.number_of_nodes(), 2))
        record += "\t" + str(nx.diameter(graph))
        record += "\t" + str(round(nx.average_shortest_path_length(graph), 2))
        open("../bbsnm-" + myear + "/stats-summary.txt", "a").write(record + "\n")

    def write_distributed_tasks(self, network):
        import networkx as nx
        import utilities
        max_no = 0
        graph = nx.read_gml("../bbsnm-" + self.year + "/" + network + ".gml")
        skill_freq = dict()
        total = 0
        skill_experts = utilities.get_skill_experts_dict(graph)
        for skill in skill_experts:
            if len(skill_experts[skill]) in skill_freq:  # skill with same number of experts
                skill_freq[len(skill_experts[skill])] += 1
            else:
                skill_freq[len(skill_experts[skill])] = 1
            total += len(skill_experts[skill])
        skill_experts = utilities.get_skill_experts_dict(graph)
        experts_per_skill = round(total / len(skill_experts), 2)
        popular_skills = set()
        unusual_skills = set()
        rare_skills = set()
        for skill in skill_experts:
            if len(skill_experts[skill]) >= experts_per_skill:
                popular_skills.add(skill)
            else:
                if len(skill_experts[skill]) <= 4:
                    rare_skills.add(skill)
                else:
                    unusual_skills.add(skill)  # rare skills
        rec = ""
        rec += str(len(popular_skills)) + "\t"
        rec += str(len(unusual_skills)) + "\t"
        rec += str(len(rare_skills)) + "\t"
        print(network + "\t" + rec + "\n")
        for tot_skl in [10, 15, 20]:
            usual_skills_list = list(popular_skills)
            unusual_skills_list = list(unusual_skills)
            import random
            import glob
            for _ in range(3):
                file_list = glob.glob("../bbsnm-" + self.year + "/" + network + "-" + str(tot_skl) + "-*.txt")
                if len(file_list) >= 3:
                    print("please delete existing(old) files")
                    break
                elif len(file_list) > 0:
                    max_no = len(file_list)
                    file_path = "../bbsnm-" + self.year + "/" + network + "-" + str(tot_skl) + "-" + str(
                        max_no) + ".txt"
                else:
                    file_path = "../bbsnm-" + self.year + "/" + network + "-" + str(tot_skl) + "-" + str(
                        max_no) + ".txt"
                open(file_path, "w").close()
                if len(popular_skills) < tot_skl:
                    print("short of common skills : " + network)
                    return
                for i in range(tot_skl):
                    tasks = []
                    for run in range(10):
                        task = set()
                        for j in range(tot_skl - i):
                            while len(task) <= j <= len(popular_skills):
                                task.add(random.choice(usual_skills_list))
                        for k in range(i):
                            while len(task) < tot_skl:
                                task.add(random.choice(unusual_skills_list))
                        tasks.append(task)
                    for task in tasks:
                        for skill in task:
                            open(file_path, "a").write(skill + "\t")
                        open(file_path, "a").write("\n")


def multiprocessing_func(network):
    # nyear = "2015"
    # dblp_dt = DBLPData(nyear)
    # dblp_dt.write_authors_info(network)
    # dblp_dt.write_titles_info(network)
    # dblp_dt.write_skills_info(network)
    # dblp_dt.build_graph(network)
    # dblp_dt.generate_network_tasks(network, 17)
    # dblp_dt.generate_network_tasks(network, 170)
    print(network)
    pass


if __name__ == '__main__':
    start_time = time.time()
    import networkx as nx

    myear = "2015"
    dblp_dt = DBLPData(myear)
    for network in ["db", "vldb", "sigmod", "icde", "icdt", "pods", "edbt"]:
        dblp_dt.write_authors_info(network)
        dblp_dt.write_titles_info(network)
        dblp_dt.write_skills_info(network)
        dblp_dt.build_graph(network)
        dblp_dt.generate_random_tasks(network, 170)
        dblp_dt.analysis(network)
        # dblp_dt.alpha_diversity(network)
        dblp_dt.write_statistics(network)
        dblp_dt.generate_distributed_tasks(network)
    # processes = []
    # for mnetwork in ["icdt", "pods", "edbt", "vldb", "icde", "sigmod"]:
    #     p = multiprocessing.Process(target=multiprocessing_func, args=(txt,))
    #     processes.append(p)
    #     p.start()
    # for process in processes:
    #     process.join()
    tqdm.write('Time taken = {} seconds'.format(time.time() - start_time))
