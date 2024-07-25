import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import PhotoImage
from PIL import Image, ImageTk

class Error:
    def __init__(self, root, message):
        self.message = message
        self.root = root

        self.canvas = ctk.CTkFrame(self.root, width=150, height=50, bg_color="red")
        self.canvas.pack(pady=5)

        self.text = ctk.CTkLabel(self.canvas, text=self.message, text_color="white", bg_color="red")
        self.text.pack()

        self.self_destruct()

    def self_destruct(self):
        self.root.after(3000, self.canvas.destroy)