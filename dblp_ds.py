# import multiprocessing
import time
from tqdm import tqdm


class DBLPRecord:

    def __init__(self):
        self.title = ""
        self.authors = set()
        self.year = ""
        self.journal = ""


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
            with open("../dblp-" + self.year + "/dblp-authors.txt", "r") as file:
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
                open("../dblp-" + self.year + "/" + network + "-titles.txt", "a").write(str(title_id) + "\t" + title + "\n")
                title_id += 1
        else:
            dblp_title_name_id_dict = dict()
            with open("../dblp-" + self.year + "/dblp-titles.txt", "r") as file:
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
                open("../dblp-" + self.year + "/" + network + "-titles.txt", "a").write(str(title_id) + "\t" + title_id_name_dict[title_id] + "\n")


    def write_skills_info(self):
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
        title_id_name_dict = dict()
        with open("../dblp-" + self.year + "/sigmod-titles.txt", "r") as file:
            for line in file:
                words = line.strip("\n").split("\t")
                title_id_name_dict[words[0]] = words[1]
        author_id_name_dict = dict()
        author_name_id_dict = dict()
        with open("../dblp-" + self.year + "/sigmod-authors.txt", "r") as file:
            for line in file:
                words = line.strip("\n").split("\t")
                author_id_name_dict[words[0]] = words[1]
                author_name_id_dict[words[1]] = words[0]
        author_id_skill_ids_dict = dict()
        author_id_pubs_dict = dict()
        collaborations_dict = dict()
        with open("../dblp-" + self.year + "/sigmod.txt") as file:
            n_lines = utilities.get_num_lines("../dblp-" + self.year + "/sigmod.txt")
            open("../dblp-" + self.year + "/sigmod-rec.txt", "w").close()
            tqdm.write("processing ../dblp-" + self.year + "/sigmod.txt - skills info ")
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
                        title_key = utilities.get_key(title_id_name_dict, title)
                        if author_name_id_dict[author] in author_id_pubs_dict:
                            if title_key in author_id_pubs_dict[author_name_id_dict[author]]:
                                pass
                            else:
                                author_id_pubs_dict[author_name_id_dict[author]].append(title_key)
                        else:
                            author_id_pubs_dict[author_name_id_dict[author]] = list()
                            author_id_pubs_dict[author_name_id_dict[author]].append(title_key)
                    if len(authors) > 1:
                        for collaborator_1 in authors:
                            for collaborator_2 in authors:
                                if collaborator_1 != collaborator_2:
                                    if collaborator_1 in author_name_id_dict and collaborator_2 in author_name_id_dict:
                                        title_key = utilities.get_key(title_id_name_dict, title)
                                        if str(author_name_id_dict[collaborator_1]) + ":" + str(
                                                author_name_id_dict[collaborator_2]) in collaborations_dict:
                                            if title_key is not None and title_key not in collaborations_dict[
                                                str(author_name_id_dict[collaborator_1]) + ":" + str(
                                                    author_name_id_dict[collaborator_2])]:
                                                collaborations_dict[
                                                    str(author_name_id_dict[collaborator_1]) + ":" + str(
                                                        author_name_id_dict[collaborator_2])].append(title_key)
                                            else:
                                                pass
                                        elif str(author_name_id_dict[collaborator_2]) + ":" + str(
                                                author_name_id_dict[collaborator_1]) in collaborations_dict:
                                            if title_key is not None and title_key not in collaborations_dict[
                                                str(author_name_id_dict[collaborator_2]) + ":" + str(
                                                    author_name_id_dict[collaborator_1])]:
                                                collaborations_dict[
                                                    str(author_name_id_dict[collaborator_2]) + ":" + str(
                                                        author_name_id_dict[collaborator_1])].append(title_key)
                                            else:
                                                pass
                                        elif title_key is not None:
                                            collaborations_dict[str(author_name_id_dict[collaborator_2]) + ":" + str(
                                                author_name_id_dict[collaborator_1])] = list()
                                            collaborations_dict[str(author_name_id_dict[collaborator_2]) + ":" + str(
                                                author_name_id_dict[collaborator_1])].append(title_key)
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
                    open("../dblp-" + self.year + "/sigmod-rec.txt", "a").write(record)
        tqdm.write("writing ../dblp-" + self.year + "/sigmod.txt -  author collaborations info ")
        open("../dblp-" + self.year + "/sigmod-author-pair-collaborations.txt", "w").close()
        for collab in tqdm(collaborations_dict, total=len(collaborations_dict)):
            open("../dblp-" + self.year + "/sigmod-author-pair-collaborations.txt", "a").write(
                str(collab) + "\t" + ",".join(collaborations_dict[collab]) + "\n")
        tqdm.write("writing ../dblp-" + self.year + "/sigmod.txt - writing author publications info ")
        open("../dblp-" + self.year + "/sigmod-author-publications.txt", "w").close()
        for author in tqdm(author_id_pubs_dict, total=len(author_id_pubs_dict)):
            open("../dblp-" + self.year + "/sigmod-author-publications.txt", "a").write(
                str(author) + "\t" + ",".join(author_id_pubs_dict[author]) + "\n")
        import os
        open("../dblp-" + self.year + "/sigmod-records.txt", "w").close()
        os.system("sort ../dblp-" + self.year + "/sigmod-rec.txt > ../dblp-" + self.year + "/sigmod-records.txt")
        os.system("rm -v ../dblp-" + self.year + "/sigmod-rec.txt >> /dev/null")
        skill_set = set()
        author_id_skills_dict = dict()
        for author in tqdm(author_id_pubs_dict, total=len(author_id_pubs_dict)):
            pub_s = ""
            author_id_skills_dict[author] = list()
            for pub in author_id_pubs_dict[author]:
                pub_s += " " + title_id_name_dict[pub]
            for skill in utilities.get_skills(pub_s):
                skill_set.add(skill)
                author_id_skills_dict[author].append(skill)
        skill_id = 1
        skill_id_name_dict = dict()
        skill_name_id_dict = dict()
        open("../dblp-" + self.year + "/sigmod-skills.txt", "w").close()
        for skill in skill_set:
            skill_id_name_dict[skill_id] = skill
            skill_name_id_dict[skill] = skill_id
            open("../dblp-" + self.year + "/sigmod-skills.txt", "a").write(str(skill_id) + "\t" + skill + "\n")
            skill_id += 1
        tqdm.write("writing ../dblp-" + self.year + "/sigmod.txt - writing author skills info ")
        open("../dblp-" + self.year + "/sigmod-author-skills.txt", "w").close()
        for author in tqdm(author_id_skills_dict, total=len(author_id_skills_dict)):
            author_id_skill_ids_dict[author] = list()
            for skill in author_id_skills_dict[author]:
                author_id_skill_ids_dict[author].append(skill_name_id_dict[skill])
            if len(author_id_skill_ids_dict[author]) > 0:
                open("../dblp-" + self.year + "/sigmod-author-skills.txt", "a").write(
                    str(author) + "\t" + ",".join([str(intg) for intg in author_id_skill_ids_dict[author]]) + "\n")

    def build_graph(self, network):
        import matplotlib.pyplot as plt
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
        for author in author_id_skill_ids_dict:
            graph.add_node(author, name=author_id_name_dict[author], skills=author_id_skill_ids_dict[author])
        for collab in collab_id_pub_ids_dict:
            u = collab.split(":")[0]
            v = collab.split(":")[1]
            num = len(collab_id_pub_ids_dict[collab].split(","))
            den = len(author_id_pub_ids_dict[u].split(",")) + len(author_id_pub_ids_dict[v].split(",")) - num
            jd = round(num / den, 3)
            graph.add_edge(u, v, weight=jd)
        largest_cc = graph.subgraph(max([cc for cc in nx.connected_components(graph)])).copy()
        nx.draw_circular(largest_cc, with_labels=True)
        nx.write_gml(largest_cc, "../dblp-" + self.year + "/" + network + ".gml")
        plt.show()


# def make_community_reocrds_file(t_name):
#     #     publicationsRecord = publicationsRecord()
#     authors_dict = dict()  # author name is key and id are values
#     authors_id_dict = dict()  # author id is key and name are values
#     authors_publications_dict = dict()
#     authors_skills_dict = dict()
#     collaborations_dict = dict()
#     import utilities
#     import networkx as nx
#     mgraph = nx.read_gml("../dblp-" + self.year + "/jdblp.gml")
#     dblp_authors_dict = dict()
#     for node in mgraph.nodes():
#         dblp_authors_dict[mgraph.nodes[node]["nname"]] = node
#     with open("../dblp-"+self.year+"/dblp.txt") as file:
#         n_lines = get_num_lines("../dblp-"+self.year+"/dblp.txt")
#         open("../dblp-"+self.year+"/dblp-rec.txt", "w").close()
#         for line in tqdm(file, total=n_lines):
#             year = ""
#             if "<year>" in line:
#                 year = line[line.index("<year>") + len("<year>"):line.index("</year>")]
#             else:
#                 pass
#             title = ""
#             if "<title>" in line:
#                 title = line[line.index("<title>") + len("<title>"):line.index("</title>") - 1]
#             else:
#                 pass
#             authors = list()
#             if "<author>" in line:
#                 authors = line[line.index("<author>") + len("<author>"):line.index("</author>")].split(":")
#                 for author in authors:
#                     if author in authors_dict.values():
#                         if title in authors_publications_dict[authors_id_dict[author]]:
#                             pass
#                         else:
#                             authors_publications_dict[authors_id_dict[author]].append(title)
#                         pass
#                     else:
#                         if author in dblp_authors_dict.keys():
#                             if author not in authors_dict:
#                                 authors_dict[author] = dblp_authors_dict[author]
#                             if authors_dict[author] not in authors_id_dict:
#                                 authors_id_dict[authors_dict[author]] = author
#                             if dblp_authors_dict[author] not in authors_publications_dict:
#                                 authors_publications_dict[dblp_authors_dict[author]] = []
#                                 authors_publications_dict[dblp_authors_dict[author]].append(title)
#                 if len(authors) > 1:
#                     for collaborator_1 in authors:
#                         for collaborator_2 in authors:
#                             if collaborator_1 != collaborator_2:
#                                 if collaborator_1 in authors_dict and collaborator_2 in authors_dict:
#                                     if str(authors_dict[collaborator_1]) + ":" + str(
#                                             authors_dict[collaborator_2]) in collaborations_dict:
#                                         if title not in collaborations_dict[
#                                             str(authors_dict[collaborator_1]) + ":" + str(
#                                                 authors_dict[collaborator_2])]:
#                                             collaborations_dict[str(authors_dict[collaborator_1]) + ":" + str(
#                                                 authors_dict[collaborator_2])].append(title)
#                                         else:
#                                             pass
#                                     elif str(authors_dict[collaborator_2]) + ":" + str(
#                                             authors_dict[collaborator_1]) in collaborations_dict:
#                                         if title not in collaborations_dict[
#                                             str(authors_dict[collaborator_2]) + ":" + str(
#                                                 authors_dict[collaborator_1])]:
#                                             collaborations_dict[str(authors_dict[collaborator_2]) + ":" + str(
#                                                 authors_dict[collaborator_1])].append(title)
#                                         else:
#                                             pass
#                                     else:
#                                         collaborations_dict[str(authors_dict[collaborator_2]) + ":" + str(
#                                             authors_dict[collaborator_1])] = list()
#                                         collaborations_dict[str(authors_dict[collaborator_2]) + ":" + str(
#                                             authors_dict[collaborator_1])].append(title)
#                                 else:
#                                     pass
#             else:
#                 pass
#             journal = ""
#             if "<journal>" in line:
#                 journal = line[line.index("<journal>") + len("<journal>"):line.index("</journal>")]
#             else:
#                 pass
#             if "<booktitle>" in line:
#                 journal = line[line.index("<booktitle>") + len("<booktitle>"):line.index("</booktitle>")]
#             else:
#                 pass
#             if len(year) > 0 and int(year) > 1999 and len(authors) > 0 and len(title) > 0 and len(journal) > 0:
#                 record = year
#                 record += "\t" + journal
#                 record += "\t" + ":".join(authors)
#                 record += "\t" + title + "\n"
#                 open("../dblp-"+self.year+"/dblp-rec.txt", "a").write(record)
#     import os
#     open("../dblp-"+self.year+"/dblp-records.txt", "w").close()
#     os.system('sort ../dblp-" + self.year + "/sigmod-rec.txt > ../dblp-" + self.year + "/sigmod-records.txt')
#     os.system('rm -v ../dblp-" + self.year + "/sigmod-rec.txt')
#     open("../dblp-"+self.year+"/dblp-authors.txt", "w").close()
#     for aid in authors_dict.keys():
#         open("../dblp-"+self.year+"/dblp-authors.txt", "a").write(str(aid) + "\t" + authors_dict[aid] + "\n")
#     open("../dblp-"+self.year+"/dblp-authors-publications.txt", "w").close()
#     open("../dblp-"+self.year+"/dblp-authors-skills.txt", "w").close()
#     skills_set = set()
#     for aid in tqdm(authors_publications_dict, total=len(authors_publications_dict)):
#         open("../dblp-"+self.year+"/dblp-authors-publications.txt", "a").write(
#             str(aid) + "\t" + " ".join(authors_publications_dict[aid]) + "\n")
#         skills = utilities.get_cmnt_skills(" ".join(authors_publications_dict[aid]))
#         for skl in skills:
#             skills_set.add(skl)
#         skills_dict = dict()
#         skills_id_dict = dict()
#         skill_id = 1
#         for skill in sorted(skills_set):
#             skills_dict[skill] = skill_id
#             skills_id_dict[skill_id] = skill
#             skill_id += 1
#     open("../dblp-"+self.year+"/dblp-skills.txt", "w").close()
#     for sid in skills_id_dict.keys():
#         open("../dblp-"+self.year+"/dblp-skills.txt", "a").write(str(sid) + "\t" + str(skills_id_dict[sid]) + "\n")
#     for aid in authors_publications_dict.keys():
#         expert_skills = utilities.get_cmnt_skills(" ".join(authors_publications_dict[aid]))  # skill names
#         skills = [str(skills_dict[skill]) for skill in expert_skills]  # skill ids
#         if len(skills) > 1:  # expert with at least two skills
#             authors_skills_dict[aid] = skills
#             open("../dblp-"+self.year+"/dblp-authors-skills.txt", "a").write(str(aid) + "\t" + ",".join(skills) + "\n")
#     open("../dblp-"+self.year+"/dblp-authors-pair.txt", "w").close()
#     for pair in collaborations_dict:
#         if len(collaborations_dict[pair]) > 1:  # authors pair with at least two collaborations
#             open("../dblp-"+self.year+"/dblp-authors-pair.txt", "a").write(
#                 str(pair) + "\t" + str(len(collaborations_dict[pair])) + "\n")
#     import networkx as nx
#     graph = nx.Graph()
#     for node in authors_dict:
#         if node in authors_skills_dict:
#             graph.add_node(node, nname=authors_dict[node], skills=",".join(authors_skills_dict[node]))
#         else:
#             graph.add_node(node, nname=authors_dict[node], skills="")
#     for pair in collaborations_dict:
#         denominator = len(authors_publications_dict[int(pair.split(":")[0])]) + len(
#             authors_publications_dict[int(pair.split(":")[1])]) - len(collaborations_dict[pair])
#         jd = 1 - (len(collaborations_dict[pair]) / denominator)
#         graph.add_edge(int(pair.split(":")[0]), int(pair.split(":")[1]), weight=jd)
#     largest_cc = nx.subgraph(graph, max(nx.connected_components(graph), key=len)).copy()
#     nx.write_gml(largest_cc, "../dblp-" + self.year + "/jdblp.gml")


# def multiprocessing_func(l_txt):
#     make_community_reocrds_file(l_txt)


if __name__ == '__main__':
    start_time = time.time()
    myear = "2015"
    network = "dblp"
    dblp_data = DBLP_Data(myear)
    # dblp_data.write_authors_info(network)
    # dblp_data.write_titles_info(network)
    # dblp_data.write_skills_info(network)
    dblp_data.build_graph(network)
    # processes = []
    # for txt in ["sigmod"]:
    #     p = multiprocessing.Process(target=multiprocessing_func, args=(txt,))
    #     processes.append(p)
    #     p.start()
    # for process in processes:
    #     process.join()
    tqdm.write('Time taken = {} seconds'.format(time.time() - start_time))
