import tkinter as tk
from tkinter import ttk
from menus.newword import *
from mediator import Mediator


class Bprogress:
    def __init__(self, root):
        self.mediator = Mediator()
        self.new_word_button = ttk.Button(root, text="Progress", command=self.show_progress)
        self.new_word_button.place(x=850, y=35)

    def show_progress(self):
        self.mediator.publish("animate")
