import tkinter as tk
from tkinter import ttk
from buttons.Bnewword import Bnewword
from buttons.Bprogress import Bprogress
from buttons.Bnewcard import Bnewcard
from menus.newword import *
from menus.flashcard import *
from menus.progress import *
from progressbar import *
from wordframe import *
from recentlytrained import RecentlyTrained


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Application")
        self.mediator = Mediator()
        self.mediator.subscribe("error", self.spawn_error)

        self.root.bind('<Button-1>', self.start_move)
        self.root.bind('<B1-Motion>', self.do_move)

        Bprogress(root)
        Bnewcard(root)
        Bnewword(root)
        ProgressBar(root)
        RecentlyTrained(root)
        Progress(root)

        self.root.after(10000, self.root.deiconify())

    def spawn_error(self, message):
        Error(self.root, message)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        self.root.geometry(f"+{self.root.winfo_x() + deltax}+{self.root.winfo_y() + deltay}")

def main():
    root = tk.Tk()
    root.geometry("1000x800")
    root.withdraw()
    root.overrideredirect(True)
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()