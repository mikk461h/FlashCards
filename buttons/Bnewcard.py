import customtkinter as ctk
from menus.newword import *
from WordHandler import *
from menus.flashcard import *


class Bnewcard:
    def __init__(self, root):
        self.root = root
        self.db = WordHandler()
        self.new_word_button = ctk.CTkButton(root, text="FLASHCARD", fg_color="purple", hover_color="orange",
                                            width=200,
                                            height=70, 
                                            corner_radius=32,
                                            border_color="white",
                                            border_width=2,
                                            command=self.random_card)
        self.new_word_button.place(x=650, y=400)
        self.mediator = Mediator()

        
    def random_card(self):
        self.mediator.publish("connect")
        new_card = self.db.random_element()
        if new_card != None:
            Flashcard(new_card[0], new_card[1], new_card[2])
        else:
            self.mediator.publish("error", "No card available!")
        self.mediator.publish("connect")
