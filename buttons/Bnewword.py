import customtkinter as ctk
from menus.newword import *

class Bnewword:
    def __init__(self, root):
        self.root = root
        self.new_word_button = ctk.CTkButton(root, text="+New", command=self.new_word, hover_color="orange", fg_color="purple",
                                            border_color="white",
                                            border_width=2,
                                            width=25, 
                                            corner_radius=32)
        self.new_word_button.place(x=40, y=35)

    def new_word(self):
        NewWord(self.root)

