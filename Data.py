# import multiprocessing
import time
from tqdm import tqdm


class DBLPRecord:

    def __init__(self):
        self.title = ""
        self.authors = set()
        self.year = ""
        self.journal = ""


class DBLPdata:

    def write_authors_info(self, t_name):
        import utilities
        authors_name_set = set()
        with open("../dblp-2015/" + t_name + ".txt") as file:
            n_lines = utilities.get_num_lines("../dblp-2015/" + t_name + ".txt")
            open("../dblp-2015/" + t_name + "-rec.txt", "w").close()
            print("processing ../dblp-2015/" + t_name + ".txt - writing authors info ")
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
        open("../dblp-2015/" + t_name + "-authors.txt", "w").close()
        for author in authors_name_set:
            author_id_name_dict[author_id] = author
            author_name_id_dict[author] = author_id
            open("../dblp-2015/" + t_name + "-authors.txt", "a").write(str(author_id) + "\t" + author + "\n")
            author_id += 1

    def write_titles_info(self, t_name):
        import utilities
        titles_set = set()
        with open("../dblp-2015/" + t_name + ".txt") as file:
            n_lines = utilities.get_num_lines("../dblp-2015/" + t_name + ".txt")
            open("../dblp-2015/" + t_name + "-rec.txt", "w").close()
            print("processing ../dblp-2015/" + t_name + ".txt - writing titles info ")
            for line in tqdm(file, total=n_lines):
                if "<title>" in line:
                    title = line[line.index("<title>") + len("<title>"):line.index("</title>") - 1]
                    if title not in titles_set:
                        titles_set.add(title)
                    else:
                        pass
        title_id = 1
        title_id_name_dict = dict()
        open("../dblp-2015/" + t_name + "-titles.txt", "w").close()
        for title in titles_set:
            title_id_name_dict[title_id] = title
            open("../dblp-2015/" + t_name + "-titles.txt", "a").write(str(title_id) + "\t" + title + "\n")
            title_id += 1

    def write_skills_info(self, t_name):
        import utilities
        title_id_name_dict = dict()
        with open("../dblp-2015/" + t_name + "-titles.txt", "r") as file:
            for line in file:
                words = line.strip("\n").split("\t")
                title_id_name_dict[words[0]] = words[1]
        author_id_name_dict = dict()
        author_name_id_dict = dict()
        with open("../dblp-2015/" + t_name + "-authors.txt", "r") as file:
            for line in file:
                words = line.strip("\n").split("\t")
                author_id_name_dict[words[0]] = words[1]
                author_name_id_dict[words[1]] = words[0]
        author_id_skill_ids_dict = dict()
        author_id_pubs_dict = dict()
        collaborations_dict = dict()
        with open("../dblp-2015/" + t_name + ".txt") as file:
            n_lines = utilities.get_num_lines("../dblp-2015/" + t_name + ".txt")
            open("../dblp-2015/" + t_name + "-rec.txt", "w").close()
            print("processing ../dblp-2015/" + t_name + ".txt - writing skills info ")
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
                        title_key = get_key(title_id_name_dict, title)
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
                                        title_key = get_key(title_id_name_dict, title)
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
                if len(year) > 0 and int(year) > 1999 and len(authors) > 0 and len(title.split()) > 3 and len(journal) > 0 :
                    record = year
                    record += "\t" + journal
                    record += "\t" + ":".join(authors)
                    record += "\t" + title + "\n"
                    open("../dblp-2015/" + t_name + "-rec.txt", "a").write(record)
        import os
        open("../dblp-2015/" + t_name + "-records.txt", "w").close()
        os.system('sort ../dblp-2015/' + t_name + '-rec.txt > ../dblp-2015/' + t_name + '-records.txt')
        os.system('rm -v ../dblp-2015/' + t_name + '-rec.txt >> /dev/null')
        skill_set = set()
        # for author in author_id_pubs_dict:
        for author in tqdm(author_id_pubs_dict, total=len(author_id_pubs_dict)):
            pub_s = ""
            for pub in author_id_pubs_dict[author]:
                pub_s += " " + title_id_name_dict[pub]
            for skill in utilities.get_skills(pub_s):
                skill_set.add(skill)
        skill_id = 1
        skill_id_name_dict = dict()
        open("../dblp-2015/" + t_name + "-skills.txt", "w").close()
        for skill in skill_set:
            skill_id_name_dict[skill_id] = skill
            open("../dblp-2015/" + t_name + "-skills.txt", "a").write(str(skill_id) + "\t" + skill + "\n")
            skill_id += 1
        open("../dblp-2015/" + t_name + "-author-skills.txt", "w").close()
        for author in tqdm(author_id_pubs_dict, total=len(author_id_pubs_dict)):
            author_id_skill_ids_dict[author] = list()
            pub_s = ""
            for pub in author_id_pubs_dict[author]:
                pub_s += " " + title_id_name_dict[pub]
            for skill in utilities.get_skills(pub_s):
                author_id_skill_ids_dict[author].append(skill)
            open("../dblp-2015/" + t_name + "-author-skills.txt", "a").write(
                str(author) + "\t" + ",".join(author_id_skill_ids_dict[author]) + "\n")


# function to return key for any value
def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key


# def make_community_reocrds_file(t_name):
#     #     publicationsRecord = publicationsRecord()
#     authors_dict = dict()  # author name is key and id are values
#     authors_id_dict = dict()  # author id is key and name are values
#     authors_publications_dict = dict()
#     authors_skills_dict = dict()
#     collaborations_dict = dict()
#     import utilities
#     import networkx as nx
#     mgraph = nx.read_gml("../dblp-2015/jdblp.gml")
#     dblp_authors_dict = dict()
#     for node in mgraph.nodes():
#         dblp_authors_dict[mgraph.nodes[node]["nname"]] = node
#     with open("../dblp-2015/" + t_name + ".txt") as file:
#         n_lines = get_num_lines("../dblp-2015/" + t_name + ".txt")
#         open("../dblp-2015/" + t_name + "-rec.txt", "w").close()
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
#                 open("../dblp-2015/" + t_name + "-rec.txt", "a").write(record)
#     import os
#     open("../dblp-2015/" + t_name + "-records.txt", "w").close()
#     os.system('sort ../dblp-2015/' + t_name + '-rec.txt > ../dblp-2015/' + t_name + '-records.txt')
#     os.system('rm -v ../dblp-2015/' + t_name + '-rec.txt')
#     open("../dblp-2015/" + t_name + "-authors.txt", "w").close()
#     for aid in authors_dict.keys():
#         open("../dblp-2015/" + t_name + "-authors.txt", "a").write(str(aid) + "\t" + authors_dict[aid] + "\n")
#     open("../dblp-2015/" + t_name + "-authors-publications.txt", "w").close()
#     open("../dblp-2015/" + t_name + "-authors-skills.txt", "w").close()
#     skills_set = set()
#     for aid in tqdm(authors_publications_dict, total=len(authors_publications_dict)):
#         open("../dblp-2015/" + t_name + "-authors-publications.txt", "a").write(
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
#     open("../dblp-2015/" + t_name + "-skills.txt", "w").close()
#     for sid in skills_id_dict.keys():
#         open("../dblp-2015/" + t_name + "-skills.txt", "a").write(str(sid) + "\t" + str(skills_id_dict[sid]) + "\n")
#     for aid in authors_publications_dict.keys():
#         expert_skills = utilities.get_cmnt_skills(" ".join(authors_publications_dict[aid]))  # skill names
#         skills = [str(skills_dict[skill]) for skill in expert_skills]  # skill ids
#         if len(skills) > 1:  # expert with at least two skills
#             authors_skills_dict[aid] = skills
#             open("../dblp-2015/" + t_name + "-authors-skills.txt", "a").write(str(aid) + "\t" + ",".join(skills) + "\n")
#     open("../dblp-2015/" + t_name + "-authors-pair.txt", "w").close()
#     for pair in collaborations_dict:
#         if len(collaborations_dict[pair]) > 1:  # authors pair with at least two collaborations
#             open("../dblp-2015/" + t_name + "-authors-pair.txt", "a").write(
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
#     nx.write_gml(largest_cc, "../dblp-2015/j" + t_name + ".gml")


# def multiprocessing_func(l_txt):
#     make_community_reocrds_file(l_txt)


if __name__ == '__main__':
    starttime = time.time()
    dblpdata = DBLPdata()
    # dblpdata.write_authors_info("icdt")
    # dblpdata.write_titles_info("icdt")
    dblpdata.write_skills_info("icdt")
    # processes = []
    # for txt in ["icdt"]:
    #     p = multiprocessing.Process(target=multiprocessing_func, args=(txt,))
    #     processes.append(p)
    #     p.start()
    # for process in processes:
    #     process.join()
    print('Time taken = {} seconds'.format(time.time() - starttime))
