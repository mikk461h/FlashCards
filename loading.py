import tkinter as tk
from PIL import ImageTk, Image

class LoadingScreen(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.geometry("400x300")
        self.overrideredirect(True)
        
        self.image = Image.open("assets/sky3.jpg")
        self.image = self.image.resize((400, 300))
        
        self.loading_image = ImageTk.PhotoImage(self.image)

        self.label = tk.Label(self, image=self.loading_image)
        self.label.pack()
        
        # Set the transparent color
        self.attributes('-transparent')
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(dim) for dim in self.geometry().split('+')[0].split('x'))
        x = screen_width // 2 - size[0] // 2
        y = screen_height // 2 - size[1] // 2
        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

    def show(self):
        self.attributes('-alpha', 1.0)  
        self.deiconify()
        self.update()

    def hide(self):
        self.withdraw()  

    def destroy(self):
        super().destroy()

