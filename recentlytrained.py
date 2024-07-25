import customtkinter as ctk
from frames.recentlyframe import RecentlyFrame
from database.WordHandler import WordHandler
from mediator import Mediator


class RecentlyTrained:
    def __init__(self, root):
        self.root = root
        self.db = WordHandler()
        self.mediator = Mediator()

        self.box_frame = ctk.CTkCanvas(self.root, width=550, height=685, borderwidth=1)
        self.box_frame.place(x=50, y=75)

        self.text = ctk.CTkLabel(self.box_frame, text="Recently Trained", font=("Arial", 25))
        self.text.place(x=25, y=20)

        self.middle_frame = ctk.CTkFrame(self.box_frame, width=490, height=600, border_color="grey", border_width=1)
        self.middle_frame.place(x=25, y=50)

        self.load_words(self.db.get_all_recently())
        self.mediator.subscribe("update_recently_visited", self.call_load_words)

    def load_word(self, word):
        native, translation, progress, status, sentence, rowid = word
        word_frame = RecentlyFrame(self.middle_frame, native, translation, progress, status, sentence)
        word_frame.pack(pady=5, padx=10, fill="x")

    def load_words(self, words=None):
        for word in words:
            self.load_word(word)

    def call_load_words(self):
        self.load_words(self.db.get_all_recently())
