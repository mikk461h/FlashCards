import tkinter as tk
from tkinter import ttk
from database.WordHandler import *
from mediator import Mediator
from error import *

class NewWord:
    def __init__(self, root):
        self.mediator = Mediator()
        self.root = root
        self.box_frame = tk.Canvas(root, width=650, height=300, borderwidth=2, relief=tk.GROOVE, background="blue")
        self.box_frame.pack(padx=20, pady=20)
        self.input_area = tk.Entry(self.box_frame, width=30)
        self.T_top_info = tk.Label(self.box_frame, text="Enter Spanish Word", font=("Arial", 12))
        self.T_top_info.pack(pady=10)
        self.T_spanish_word = tk.Label(self.box_frame, text="", font=("Arial", 12))
        self.T_spanish_word.pack(pady=5)
        self.T_translation = tk.Label(self.box_frame, text="", font=("Arial", 12))
        self.T_translation.pack(pady=5)
        self.B_back = tk.Button(self.box_frame, text="Undo", command=lambda: (self.switch_state("back"), self.update_state()))
        self.B_confirm = tk.Button(self.box_frame, text="Confirm", command=self.confirm)
        self.input_area.bind('<Return>', self.handle_input)
        self.states = ["spanish", "translation", "confirm"]
        self.state = self.states[0]
        self.saved_input = []

        self.update_state()

    def update_state(self):
        self.T_top_info.config(text={
            "spanish": "Enter Spanish Word",
            "translation": "Enter Translation",
            "confirm": "Confirm"
        }.get(self.state, ""))

        if self.state == "spanish":
            self.saved_input = []
            self.T_spanish_word.config(text="")
            self.T_translation.config(text="")
            self.B_back.pack_forget()
            self.B_confirm.pack_forget()

        if self.state == "translation":
            if len(self.saved_input) > 1:
                self.saved_input.pop()
            self.T_translation.config(text="")
            self.B_back.pack(pady=10)
            self.B_confirm.pack_forget()

        if self.state == "confirm":
            self.input_area.pack_forget()
            self.B_confirm.pack(pady=10)
        else:
            self.input_area.pack(pady=10)
            self.input_area.focus()
            self.input_area.delete(0, tk.END)

    def switch_state(self, switch=None):
        if switch == "back":
            current_index = self.states.index(self.state)
            self.state = self.states[current_index - 1]
        elif switch in self.states:
            self.state = switch

    def handle_input(self, event):
        get_word = self.input_area.get()
        if get_word.strip():
            if self.state == "spanish":
                self.T_spanish_word.config(text=get_word)
                self.switch_state("translation")
                self.update_state()
            elif self.state == "translation":
                self.T_translation.config(text=get_word)
                self.switch_state("confirm")
                self.update_state()
            self.saved_input.append(get_word)
        else:
            print("no input")

    def confirm(self):
        db = WordHandler()
        add = db.add_word(self.saved_input[0], self.saved_input[1])
        if add == "word exists":
            self.mediator.publish("error", "Word already exists!")
        self.mediator.publish("update")
        self.box_frame.destroy()