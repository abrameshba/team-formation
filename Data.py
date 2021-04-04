import multiprocessing
import time
from tqdm import tqdm
import mmap


class PublicationRecord:

    def __init__(self, year, title, authors, journal):
        self.title = title
        self.authors = list()
        self.year = year
        self.journal = journal


# ref : https://blog.nelsonliu.me/2016/07/30/progress-bars-for-python-file-reading-with-tqdm/
def get_num_lines(file_path):
    fp = open(file_path, "r+")
    buf = mmap.mmap(fp.fileno(), 0)
    lines = 0
    while buf.readline():
        lines += 1
    return lines


def make_reocrds_file(t_name):
    #     publicationsRecord = publicationsRecord()
    authors_dict = dict()  # author id is key and name are values
    authors_id_dict = dict()  # author name is key and id are values
    authors_publications_dict = dict()
    authors_skills_dict = dict()
    collaborations_dict = dict()
    author_id = 1
    import utilities
    with open("../dblp-2020/" + t_name + ".txt") as file:
        n_lines = get_num_lines("../dblp-2020/" + t_name + ".txt")
        open("../dblp-2020/" + t_name + "-rec.txt", "w").close()
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
                    if author in authors_dict.values():
                        if title in authors_publications_dict[authors_id_dict[author]]:
                            pass
                        else:
                            authors_publications_dict[authors_id_dict[author]].append(title)
                        pass
                    else:
                        authors_dict[author_id] = author
                        authors_id_dict[author] = author_id
                        authors_publications_dict[author_id] = []
                        authors_publications_dict[author_id].append(title)
                        author_id += 1
                if len(authors) > 1:
                    for collaborator_1 in authors:
                        for collaborator_2 in authors:
                            if collaborator_1 != collaborator_2:
                                if str(authors_id_dict[collaborator_1]) + ":" + str(
                                        authors_id_dict[collaborator_2]) in collaborations_dict:
                                    if title not in collaborations_dict[
                                        str(authors_id_dict[collaborator_1]) + ":" + str(
                                            authors_id_dict[collaborator_2])]:
                                        collaborations_dict[str(authors_id_dict[collaborator_1]) + ":" + str(
                                            authors_id_dict[collaborator_2])].append(title)
                                    else:
                                        pass
                                elif str(authors_id_dict[collaborator_2]) + ":" + str(
                                        authors_id_dict[collaborator_1]) in collaborations_dict:
                                    if title not in collaborations_dict[
                                        str(authors_id_dict[collaborator_2]) + ":" + str(
                                            authors_id_dict[collaborator_1])]:
                                        collaborations_dict[str(authors_id_dict[collaborator_2]) + ":" + str(
                                            authors_id_dict[collaborator_1])].append(title)
                                    else:
                                        pass
                                else:
                                    collaborations_dict[str(authors_id_dict[collaborator_2]) + ":" + str(
                                        authors_id_dict[collaborator_1])] = list()
                                    collaborations_dict[str(authors_id_dict[collaborator_2]) + ":" + str(
                                        authors_id_dict[collaborator_1])].append(title)
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
            if len(year) > 0 and len(authors) > 0 and len(title) > 0 and len(journal) > 0:
                record = year
                record += "\t" + journal
                record += "\t" + ":".join(authors)
                record += "\t" + title + "\n"
                open("../dblp-2020/" + t_name + "-rec.txt", "a").write(record)
    import os
    open("../dblp-2020/" + t_name + "-records.txt", "w").close()
    os.system('sort ../dblp-2020/' + t_name + '-rec.txt > ../dblp-2020/' + t_name + '-records.txt')
    os.system('rm -v ../dblp-2020/' + t_name + '-rec.txt')
    open("../dblp-2020/" + t_name + "-authors.txt", "w").close()
    for aid in authors_dict.keys():
        open("../dblp-2020/" + t_name + "-authors.txt", "a").write(str(aid) + "\t" + authors_dict[aid] + "\n")
    open("../dblp-2020/" + t_name + "-authors-publications.txt", "w").close()
    open("../dblp-2020/" + t_name + "-authors-skills.txt", "w").close()
    skills_set = set()
    for aid in authors_publications_dict.keys():
        open("../dblp-2020/" + t_name + "-authors-publications.txt", "a").write(
            str(aid) + "\t" + " ".join(authors_publications_dict[aid]) + "\n")
        skills = utilities.get_skills(" ".join(authors_publications_dict[aid]))
        for skl in skills:
            skills_set.add(skl)
    skills_dict = dict()
    skills_id_dict = dict()
    skill_id = 1
    for skill in sorted(skills_set):
        skills_dict[skill] = skill_id
        skills_id_dict[skill_id] = skill
        skill_id += 1
    open("../dblp-2020/" + t_name + "-skills.txt", "w").close()
    for sid in skills_id_dict.keys():
        open("../dblp-2020/" + t_name + "-skills.txt", "a").write(str(sid) + "\t" + str(skills_id_dict[sid]) + "\n")
    for aid in authors_publications_dict.keys():
        expert_skills = utilities.get_skills(" ".join(authors_publications_dict[aid]))  # skill names
        skills = [str(skills_dict[skill]) for skill in expert_skills]  # skill ids
        if len(skills) > 0:  # expert with at least two skills
            authors_skills_dict[aid] = skills
            open("../dblp-2020/" + t_name + "-authors-skills.txt", "a").write(str(aid) + "\t" + ",".join(skills) + "\n")
    open("../dblp-2020/" + t_name + "-authors-pair.txt", "w").close()
    for pair in collaborations_dict:
        if len(collaborations_dict[pair]) > 1:  # authors pair with at least two collaborations
            open("../dblp-2020/" + t_name + "-authors-pair.txt", "a").write(
                str(pair) + "\t" + str(len(collaborations_dict[pair])) + "\n")
    import networkx as nx
    graph = nx.Graph()
    for node in authors_dict:
        if node in authors_skills_dict:
            graph.add_node(node, nname=authors_dict[node], skills=",".join(authors_skills_dict[node]))
        else:
            graph.add_node(node, nname=authors_dict[node], skills="")
    for pair in collaborations_dict:
        denominator = len(authors_publications_dict[int(pair.split(":")[0])]) + len(
            authors_publications_dict[int(pair.split(":")[1])]) - len(collaborations_dict[pair])
        jd = 1 - (len(collaborations_dict[pair]) / denominator)
        graph.add_edge(int(pair.split(":")[0]), int(pair.split(":")[1]), weight=jd)
    largest_cc = nx.subgraph(graph, max(nx.connected_components(graph), key=len)).copy()
    nx.write_gml(largest_cc, "../dblp-2020/" + t_name + ".gml")


def multiprocessing_func(l_txt):
    make_reocrds_file(l_txt)


if __name__ == '__main__':
    starttime = time.time()
    processes = []
    #for txt in ["articles", "inproceedings"]:
    for txt in ["vldb"]:
        p = multiprocessing.Process(target=multiprocessing_func, args=(txt,))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()
    print('Time taken = {} seconds'.format(time.time() - starttime))
