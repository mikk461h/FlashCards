import tkinter as tk
import customtkinter as ctk 
from WordHandler import *
from menus.flashcard import *

class RecentlyFrame(tk.Frame):
    def __init__(self, root, native, translation, progress, status, sentence):
        super().__init__(root, width=450, height=60)  

        self.db = WordHandler()
        self.mediator = Mediator()
        self.native = native
        self.translation = translation
        self.progress = progress
        self.status = status
        self.sentence = sentence

        self.native_label = ctk.CTkLabel(self, text=f"{native}", font=("Platino", 16, "bold"))
        self.native_label.place(x=25)

        self.translation_label = ctk.CTkLabel(self, text=f"{translation}")
        self.translation_label.place(x=25, y=25)

        self.progress_label = ctk.CTkLabel(self, text=f"{progress} / 10", font=("Arial", 16, "italic"))
        self.progress_label.place(x=125, y=17.5)

        self.B_train_card = ctk.CTkButton(self, text="Train", command=self.train, hover_color="green")
        self.B_train_card.place(x=250, y=17.5)

        self.update_color()

    def delete_word(self):
        self.db.delete_word(self.native)
        self.mediator.publish("update")
        self.destroy()

    def update_color(self):
        if self.progress >= 10:
            self.configure(background="green")
        elif self.progress > 5 and self.progress < 10:
            self.configure(background="#A37C18")

    def train(self):
       Flashcard(self.native, self.translation, self.progress)