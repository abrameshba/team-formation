import tkinter as tk
from tkinter import ttk


class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.cb = ttk.Combobox(self.container, values=[0, 1, 2, 3], state='readonly')
        self.cb.bind('<<ComboboxSelected>>', self.modified)
        self.cb.pack()

    def modified(self, event):
        print(self.cb.get())


main = Main()
main.mainloop()