import tkinter as tk
import webbrowser
import os
from tkinter import font

class About:
    def __init__(self, root):
        about = tk.Toplevel(root)
        about.title("About - JK PasswordManager")

        window_width = 600
        window_hight = 200

        monitor_width = about.winfo_screenwidth()
        monitor_hight = about.winfo_screenheight()

        x = (monitor_width / 2) - (window_width / 2)
        y = (monitor_hight / 2) - (window_hight / 2)

        about.geometry(f"{window_width}x{window_hight}+{int(x)}+{int(y)}")
        icon_image = tk.PhotoImage(file=os.path.join("assets", "icon.png"))
        about.iconphoto(True, icon_image)
        about.configure(bg="#f5f5f5")
        about.resizable(False, False)
        about.focus_force()

        custom_font = font.Font(family="Helvetica", size=12, weight="bold")

        frame = tk.Frame(about, bg="#f5f5f5")
        frame.pack(pady=50)

        text = "JK PasswordManager is an open source app created by Josakko, \nall documentation and instructions can be found on"
        label_text = tk.Label(frame, text=text, font=custom_font, bg="#f5f5f5", fg="#333333")
        label_text.pack(side=tk.LEFT)

        link_text = tk.Label(frame, text="GitHub", font=custom_font, bg="#f5f5f5", fg="#007bff", cursor="hand2")
        link_text.pack(side=tk.LEFT, anchor="sw") #side=tk.BOTTOM

        link_text.bind("<Button-1>", self.open_link)

    def open_link(self, event):
        webbrowser.open_new("https://github.com/Josakko/JK_PasswordManager")

