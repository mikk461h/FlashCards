import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from wordframe import *
from WordHandler import *
from mediator import Mediator

class Progress:
    def __init__(self, root):
        self.mediator = Mediator()
        self.root = root
        self.db = WordHandler()
        self.mediator.subscribe("update", self.load_words)
        self.mediator.subscribe("animate", self.animate)
        self.end_pos = 10
        self.start_pos = 1000
        self.pos = self.start_pos
        self.in_start_pos = True

        self.box_frame = ctk.CTkCanvas(self.root, width=990, height=685, borderwidth=1, relief=tk.GROOVE)
        self.box_frame.place(x=self.pos, y=75)

        self.middle_frame = ctk.CTkScrollableFrame(self.box_frame, width=950, height=600, border_color="grey", border_width=1)
        self.middle_frame.place(x=15, y=40)
    
        self.prev_button = ctk.CTkButton(self.box_frame, text="Previous", command=self.prev_page)
        self.next_button = ctk.CTkButton(self.box_frame, text="Next", command=self.next_page)
        self.prev_button.place(x=300, y=660)
        self.next_button.place(x=500, y=660)

        self.current_page = 0
        self.words_per_page = 25

        self.filter_var = tk.StringVar()
        self.all_checkbox = tk.Checkbutton(self.box_frame, text="All", variable=self.filter_var, onvalue="All", offvalue="", command=self.load_words)
        self.finished_checkbox = tk.Checkbutton(self.box_frame, text="Finished", variable=self.filter_var, onvalue="Finished", offvalue="", command=self.load_words)
        self.inprogress_checkbox = tk.Checkbutton(self.box_frame, text="InProgress", variable=self.filter_var, onvalue="InProgress", offvalue="", command=self.load_words)

        self.all_checkbox.place(x=300, y=10)
        self.finished_checkbox.place(x=450, y=10)
        self.inprogress_checkbox.place(x=600, y=10)

        self.sort_var = tk.StringVar(value="None")
        sort_menu = ctk.CTkOptionMenu(self.box_frame, variable=self.sort_var, values=["None", "Alphabetical", "Progress"])
        sort_menu.place(x=50, y=10)
        sort_menu.bind("<<OptionMenuSelected>>", lambda e: self.load_words())

        self.load_words()
        
    def load_word(self, word):
        native, translation, progress, status, sentence = word
        word_frame = Wordframe(self.middle_frame, native, translation, progress, status, sentence)
        word_frame.pack(pady=5, padx=10, fill="x")

    def load_words(self, words=None):
        for widget in self.middle_frame.winfo_children():
            widget.destroy()

        all_words = self.apply_filter(self.db.get_all())

        sorted_words = self.apply_sort(all_words)

        start_index = self.current_page * self.words_per_page
        end_index = start_index + self.words_per_page
        words = sorted_words[start_index:end_index]

        for word in words:
            self.load_word(word)

        self.middle_frame.update_idletasks()
        self.update_buttons(len(all_words))

    def apply_sort(self, words):
        sort_option = self.sort_var.get()
        if sort_option == "Alphabetical":
            return sorted(words, key=lambda x: x[0])
        elif sort_option == "Progress":
            return sorted(words, key=lambda x: x[2], reverse=True)
        return words
    
    def apply_filter(self, words):
        filter_option = self.filter_var.get()
        if filter_option == "Finished":
            return [word for word in words if word[2] == 10]
        elif filter_option == "InProgress":
            return [word for word in words if word[3] == 'in progress']
        return words
    
    def update_buttons(self, all_words):
        total_pages = (all_words - 1) // self.words_per_page + 1
        
        if self.current_page <= 0:
            self.prev_button.configure(state=tk.DISABLED)
        else:
            self.prev_button.configure(state=tk.NORMAL)
        
        if self.current_page >= total_pages - 1:
            self.next_button.configure(state=tk.DISABLED)
        else:
            self.next_button.configure(state=tk.NORMAL)

    def next_page(self):
        self.current_page += 1
        self.load_words()

    def prev_page(self):
        self.current_page -= 1
        self.load_words()

    def animate_forward(self):
        if self.pos < self.start_pos:
            self.pos += 35 
            self.box_frame.place(x=self.pos, y=75) 
            self.root.after(10, self.animate_forward)
        else:
            self.in_start_pos = True

    def animate_backwards(self):
        if self.pos < 0:
            self.pos = 0
            self.box_frame.place(x=self.pos, y=75) 
        if self.pos > self.end_pos:
            self.pos -= 35 
            self.box_frame.place(x=self.pos, y=75) 
            self.root.after(10, self.animate_backwards)
        else:
            self.in_start_pos = False  
            
    def animate(self):
        if self.in_start_pos:
            self.animate_backwards()
        else:
            self.animate_forward()
