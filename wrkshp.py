import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.constants import *


class wrkshp():

    def __init__(self):
        main_window = tk.Tk()
        main_window.geometry("600x700")
        main_window.title("Team Formation from social networks")
        self.top_window = ttk.Frame(main_window).grid(row=0, column=0)
        self.bottom_window = ttk.Frame(main_window).grid(row=1, column=0)
        self.makeInputFrame()
        self.makeOutputFrame()
        self.makeStatusFrame()
        main_window.mainloop()

    def makeInputFrame(self):
        import utilities
        import networkx as nx
        iframe = ttk.Labelframe(self.top_window, text="Input")
        iframe.grid(row=0, column=0)
        self.network_label = ttk.Label(iframe, text="Network : ")
        self.network_label.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
        self.network = tk.StringVar()
        self.network_box = ttk.Combobox(iframe, textvariable=self.network)
        networks = ["vldb", "sigmod", "icde", "icdt", "edbt", "pods", "db"]
        # networks = ["VLDB", "SIGMOD", "ICDE", "ICDT", "EDBT", "PODS", "WWW", "KDD", "SDM", "PKDD", "ICDM", "ICML",
        #             "ECML", "COLT", "UAI", "SODA", "FOCS", "STOC", "STACS", "DB", "DM", "AI", "TH"]
        self.network_box['values'] = networks
        self.network_box.current(0)
        self.network_current_value = self.network_box.get()
        self.network_box.state(['readonly'])
        self.network_box.bind('<<ComboboxSelected>>', self.update_skills)
        self.network_box.grid(row=0, column=1, padx=5, pady=5, sticky="NSEW")
        self.algorithm_label = ttk.Label(iframe, text="Algorithm : ")
        self.algorithm_label.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")
        self.algorithm = tk.StringVar()
        self.algorithm_box = ttk.Combobox(iframe, textvariable=self.algorithm)
        self.algorithm_box['values'] = ['TPLClosest1', 'TPLClosest2', 'TPLRandom', 'Rarestfirst', 'BestSumDistance', 'BestLeaderDistance', 'MinimumDiameterSolution']
        self.algorithm_box.current(0)
        self.algorithm_current_value = self.algorithm_box.get()
        self.algorithm_box.state(['readonly'])
        self.algorithm_box.bind('<<ComboboxSelected>>', self.update_algorithm)
        self.algorithm_box.grid(row=1, column=1, padx=5, pady=5, sticky="NSEW")
        self.skill_label = ttk.Label(iframe, text="Skills : ")
        self.skill_label.grid(row=2, column=0, padx=5, pady=5, sticky="NSEW")
        self.skills = list()
        self.yscrollbar = Scrollbar(iframe)
        self.yscrollbar.grid(row=2, column=1, padx=5, pady=5, sticky="NSEW")
        self.skill_box = tk.Listbox(iframe, height=6, selectmode="extended", yscrollcommand=self.yscrollbar.set)
        if len(self.network_current_value) > 0:
            self.graph = nx.read_gml("../dblp-2015/" + (self.network_current_value).lower() + ".gml")
            skill_experts = utilities.get_skill_experts_dict(self.graph)
            dblp_skill_name_id_dict = dict()
            with open("../dblp-2015/db-skills.txt", "r") as file:
                for line in file:
                    line_words = line.strip("\n").split()
                    dblp_skill_name_id_dict[line_words[0]] = line_words[1]
            for key in skill_experts.keys():
                self.skills.append(dblp_skill_name_id_dict[key])
        self.skills = sorted(self.skills)
        for each_item in range(len(self.skills)):
            self.skill_box.insert(END, self.skills[each_item])
            # coloring alternative lines of listbox
            self.skill_box.itemconfig(each_item,
                                      bg="yellow" if each_item % 2 == 0 else "cyan")
        self.yscrollbar.config(command=self.skill_box.yview)
        self.skill_box.grid(row=2, column=1, padx=5, pady=5, sticky="NSEW")
        self.reset_button = ttk.Button(iframe, text="Reset", command=self.reset_status)
        self.reset_button.grid(row=3, column=0, padx=5, pady=5)
        self.start_button = tk.Button(iframe, text="Start", command=self.update_status)
        self.start_button.grid(row=3, column=1, padx=5, pady=5)

    def makeOutputFrame(self):
        self.oframe = ttk.Labelframe(self.top_window, text="Output")
        self.oframe.grid(row=0, column=1)
        self.olabel1 = ttk.Label(self.oframe, text="")
        self.olabel1.grid(row=0, column=0, padx=5, pady=5)

    def makeStatusFrame(self):
        self.sframe = ttk.Labelframe(self.bottom_window, text="Status")
        self.sframe.grid(row=1, column=0, columnspan=2)
        global status_label
        status_label = tk.Label(self.sframe, text="")
        status_label.pack(fill=tk.BOTH)

    def update_status(self):
        from Team import Team
        import Algorithms
        global status_label
        import networkx as nx
        # self.network_current_value = self.network_box.get()
        # self.algorithm_current_value = self.algorithm_box.get()
        # if len(self.network_current_value) == 0:
        #     tk.messagebox.showerror('Network ?', 'Please select Network')
        # if len(self.algorithm_current_value) == 0:
        #     tk.messagebox.showerror('Algorithm ?', 'Please select Algorithm')
        # import networkx as nx
        # import utilities
        # if len(self.network_current_value) > 0:
        self.graph = nx.read_gml("../dblp-2015/" + (self.network_current_value).lower() + ".gml")
        #     skill_experts = utilities.get_skill_experts_dict(self.graph)
        #     dblp_skill_name_id_dict = dict()
        dblp_skill_id_name_dict = dict()
        with open("../dblp-2015/db-skills.txt", "r") as file:
            for line in file:
                line_words = line.strip("\n").split()
                dblp_skill_id_name_dict[line_words[1]] = line_words[0]
                # dblp_skill_name_id_dict[line_words[0]] = line_words[1]
        #     self.skills = list()
        #     for key in skill_experts.keys():
        #         self.skills.append(dblp_skill_name_id_dict[key])
        # # self.skill_box.delete(0,tk.END)
        # # for each_item in range(len(self.skills)):
        # #     self.skill_box.insert(END, self.skills[each_item])
        # #     # coloring alternative lines of listbox
        # #     self.skill_box.itemconfig(each_item,
        # #                               bg="yellow" if each_item % 2 == 0 else "cyan")
        # #     self.yscrollbar.config(command=self.skill_box.yview)
        # else:
        #     pass
        # msg = "Network : " + self.network_current_value + "\n" + "Algorithm : " + self.algorithm_current_value \
        #       + "\n" + "#Skills : " + str(len(self.skills))
        # status_label['text'] = msg
        self.team = Team()
        self.selected = []
        self.task = []
        for i in self.skill_box.curselection():
            self.selected.append(self.skill_box.get(i))
        self.olabel1['text'] = "Selected Skills : "+str(len(self.selected))+"\n"
        self.selected = sorted(self.selected)
        import time
        start = time.time()
        for skill in self.selected:
            self.task.append(dblp_skill_id_name_dict[skill])
            self.olabel1['text'] += "\n"+skill
        if self.algorithm_current_value == "Rarestfirst":
            self.olabel1['text'] += "\n\nAlgorithm : Rarestfirst\n"
            self.team = Algorithms.rarestfirst(self.graph, self.task)
        elif self.algorithm_current_value=="TPLClosest2":
            self.olabel1['text'] += "\n\nAlgorithm : TPLClosest-2\n"
            self.team = Algorithms.tfs(self.graph, self.task, 2, 2)
        elif self.algorithm_current_value=="TPLClosest1":
            self.olabel1['text'] += "\n\nAlgorithm : TPLClosest-1\n"
            self.team = Algorithms.tfs(self.graph, self.task, 1, 1)
        elif self.algorithm_current_value=="BestSumDistance":
            self.olabel1['text'] += "\n\nAlgorithm : BestSumDistance\n"
            self.team = Algorithms.best_sum_distance(self.graph, self.task)
        elif self.algorithm_current_value=="TPLRandom":
            self.olabel1['text'] += "\n\nAlgorithm : TPLRandom\n"
            self.team = Algorithms.tfr(self.graph, self.task,2,2)
        elif self.algorithm_current_value=="MinimumDiameterSolution":
            self.olabel1['text'] += "\n\nAlgorithm : MinimumDiameterSolution\n"
            self.team = Algorithms.min_diam_sol(self.graph, self.task,5)
        else:
            pass
        end = time.time()
        lst = list(self.team.experts)
        self.olabel1['text'] += "\n\nProcessing time : " + str(round(end-start,2)) + " sec \n"
        self.olabel1['text'] += "\n\nLeader : " + self.graph.nodes[self.team.leader]["name"] + "\n"
        self.olabel1['text'] += "\n\nTeam size : "+str(len(self.team.experts))+"\n"
        self.olabel1['text'] += "\n\nTeam : "+ "\n"
        for member in lst :
            self.olabel1['text'] += "\n"+self.graph.nodes[member]["name"]

    def update_algorithm(self,event):
        import networkx as nx
        # self.algorithm_box.current(self.algorithm_box.get())
        self.algorithm_current_value = self.algorithm_box.get()
        if len(self.algorithm_current_value) == 0:
            tk.messagebox.showerror('Algorithm ?', 'Please select Algorithm')
        msg = "Algorithm : " + self.algorithm_current_value + "\n" + "Number of Skills : " + str(len(self.skills)) +"\n" +str(
            nx.info(self.graph))
        status_label['text'] = msg

    def update_skills(self, event):
        global status_label
        # self.network_box.current(self.network_box.get())
        self.network_current_value = self.network_box.get()
        if len(self.network_current_value) == 0:
            tk.messagebox.showerror('Network ?', 'Please select Network')
        import networkx as nx
        import utilities
        if len(self.network_current_value) > 0:
            self.graph = nx.read_gml("../dblp-2015/" + (self.network_current_value).lower() + ".gml")
            skill_experts = utilities.get_skill_experts_dict(self.graph)
            dblp_skill_name_id_dict = dict()
            dblp_skill_id_name_dict = dict()
            with open("../dblp-2015/db-skills.txt", "r") as file:
                for line in file:
                    line_words = line.strip("\n").split()
                    dblp_skill_name_id_dict[line_words[0]] = line_words[1]
                    dblp_skill_id_name_dict[line_words[1]] = line_words[0]
            self.skills = list()
            for key in skill_experts.keys():
                self.skills.append(dblp_skill_name_id_dict[key])
        self.skills = sorted(self.skills)
        self.skill_box.delete(0,tk.END)
        for each_item in range(len(self.skills)):
            self.skill_box.insert(END, self.skills[each_item])
            # coloring alternative lines of listbox
            self.skill_box.itemconfig(each_item,
                                      bg="yellow" if each_item % 2 == 0 else "cyan")
            self.yscrollbar.config(command=self.skill_box.yview)
        else:
            pass
        msg = "Algorithm : " + self.algorithm_current_value + "\n" + "Number of Skills : " + str(len(self.skills)) +"\n" +str(
            nx.info(self.graph))
        status_label['text'] = msg

    def reset_status(self):
        global status_label
        self.network_box.current(0)
        self.algorithm_box.current(0)
        self.network_current_value = self.network_box.get()
        self.algorithm_current_value = self.algorithm_box.get()
        import networkx as nx
        import utilities
        if len(self.network_current_value) > 0:
            self.graph = nx.read_gml("../dblp-2015/" + (self.network_current_value).lower() + ".gml")
            skill_experts = utilities.get_skill_experts_dict(self.graph)
            dblp_skill_name_id_dict = dict()
            with open("../dblp-2015/db-skills.txt", "r") as file:
                for line in file:
                    line_words = line.strip("\n").split()
                    dblp_skill_name_id_dict[line_words[0]] = line_words[1]
            self.skills = list()
            for key in skill_experts.keys():
                self.skills.append(dblp_skill_name_id_dict[key])
        self.skills = sorted(self.skills)
        self.skill_box.delete(0,tk.END)
        for each_item in range(len(self.skills)):
            self.skill_box.insert(END, self.skills[each_item])
            # coloring alternative lines of listbox
            self.skill_box.itemconfig(each_item,
                                      bg="yellow" if each_item % 2 == 0 else "cyan")
            self.yscrollbar.config(command=self.skill_box.yview)
        else:
            pass
        msg = "Algorithm : " + self.algorithm_current_value + "\n" + "Number of Skills : " + str(len(self.skills)) +"\n" +str(
            nx.info(self.graph))
        status_label['text'] = msg
        self.olabel1['text'] = ""


app = wrkshp()
