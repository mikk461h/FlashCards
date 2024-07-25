import tkinter as tk
from tkinter import ttk
from WordHandler import *
from mediator import *

class ProgressBar:
    def __init__(self, parent):
        self.parent = parent
        self.db = WordHandler()
        self.mediator = Mediator()

        self.progressbar = ttk.Progressbar(self.parent, orient="horizontal", length=500, mode="determinate")
        self.progressbar.place(x=250, y=40)

        self.progressbar['maximum'] = 6000
        self.progressbar['value'] = 0

        self.total_words(self.parent)
        self.progress_updater(self.parent)
        self.mediator.subscribe("update", self.mediator_function)

    def total_words(self, root):
        words = self.db.get_all()
        self.T_words = tk.Label(root, text="words: " + str(len(words)), font=("Arial", 15))
        self.T_words.place(x=170, y=35)

    def progress_updater(self, root):
        finished = self.db.get_finished()
        self.progressbar['value'] = len(finished)
        self.T_finished = tk.Label(root, text=str(len(finished)) + "/6000", font=("Arial", 15))
        self.T_finished.place(x=775, y=35)

    def mediator_function(self):
        self.total_words(self.parent)
        self.progress_updater(self.parent)

