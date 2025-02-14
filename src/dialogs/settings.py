import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os


class Settings:
    def __init__(self, dashboard):
        self.db = dashboard.db
        self.dashboard = dashboard

        self.settings = Toplevel(self.dashboard)

        settings_width = 400
        settings_hight = 500

        monitor_width = self.settings.winfo_screenwidth()
        monitor_hight = self.settings.winfo_screenheight()

        x = (monitor_width / 2) - (settings_width / 2)
        y = (monitor_hight / 2) - (settings_hight / 2) - 150

        self.settings.geometry(f"{settings_width}x{settings_hight}+{int(x)}+{int(y)}")
        self.settings.title("Settings")

        icon_image = tk.PhotoImage(file=os.path.join("assets", "icon.png"))
        self.settings.iconphoto(True, icon_image)
        self.settings.resizable(False, False)
        
        self.settings.focus_force()
        # self.settings.grab_set()
        font = ("Arial", 12)

        export_button = tk.Button(self.settings, text="Export to CSV", command=self.dashboard.export, relief="raised", width=15, font=font)
        export_button.pack(pady=10, padx=15, side="right")
        
        import_button = tk.Button(self.settings, text="Import from CSV", command=self.dashboard.import_, relief="raised", width=15, font=font)
        import_button.pack(pady=10, padx=15, side="right")
        
        
        self.settings.mainloop()

