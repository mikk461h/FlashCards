import tkinter as tk
from tkinter import ttk
from WordHandler import *
from mediator import Mediator
from error import *

class Flashcard:
    def __init__(self, native, translation, progress):
        self.native = native
        self.translation = translation
        self.progress = progress
        self.db = WordHandler()
        self.mediator = Mediator()

        self.box_frame = tk.Canvas(width=1000, height=800)
        self.box_frame.place(x=0, y=0)
        self.box_frame.bind("<Button-1>", lambda event: self.box_frame.destroy())
        
        self.box = tk.Canvas(self.box_frame, width=400, height=250, borderwidth=2, relief=tk.GROOVE, background="orange")
        self.box.place(x=280, y=275)
        self.box.bind("<Button-1>", lambda event: self.switch_state())

        self.T_word = tk.Label(self.box, text=self.native, font=("Arial", 24))
        self.T_word.place(x=170, y=115)

        self.T_progess = tk.Label(self.box, text=str(self.progress) + "/10", font=("Arial", 10))
        self.T_progess.place(x=25, y=25)

        self.B_yes = tk.Button(self.box_frame, text="Yes!", font=("Arial", 12), command=self.yes_command)
        self.B_yes.place(x=300, y=550)
        self.B_no = tk.Button(self.box_frame, text="No!", font=("Arial", 12), command=self.no_command)
        self.B_no.place(x=610, y=550)

        self.states = ["native", "translation"]
        self.state = self.states[0]

    
    def update_state(self):
        self.T_word.config(text={
            "native": self.native,
            "translation": self.translation,
        }.get(self.state, ""))

    def switch_state(self):
        current_index = self.states.index(self.state)
        self.state = self.states[current_index - 1]
        self.update_state()

    def no_command(self):
        new_card = self.db.random_element()
        if new_card != None:
            Flashcard(new_card[0], new_card[1], new_card[2])
        else:
            self.mediator.publish("error", "No card available!")
        self.destroy_frame()

    def yes_command(self):
        self.db.update_progress(self.native)
        self.db.add_to_visited(self.native)
        self.mediator.publish("update_recently_visited")
        new_card = self.db.random_element()
        print(new_card)
        if new_card != None:
            Flashcard(new_card[0], new_card[1], new_card[2])
        else:
            self.mediator.publish("error", "No card available!")
        self.destroy_frame()

    def destroy_frame(self):
        print("Destroying frame!")
        self.mediator.publish("update")
        self.box_frame.destroy()