import tkinter as tk 
from handlers.login_handler import LoginHandler
from app_database import database as db
from PIL import ImageTk, Image
import requests
import webbrowser
from tkinter import messagebox
#from generator import PasswordGenerator


#!######### VERSION #########!#
VERSION = "v6"
#!######### VERSION #########!#


def check_version(version):
    url = "https://api.github.com/repos/Josakko/JK_PasswordManager/releases/latest"
    try: res = requests.get(url)
    except: return
    
    if res.status_code == 200:
        res = res.json()
        latest_ver = res["tag_name"]
        if latest_ver != version:
            return res["html_url"]
        else:
            return False
    else:
        return False
    
latest_version = check_version(VERSION)
if latest_version:
    choice = messagebox.askyesno("Update", "Looks like new version is available, do you want to update now?")
    if choice:
        webbrowser.open_new(latest_version)


class JK_Password_Manager:
    def __init__(self, root):
        self.root = root
        self.root.minsize(750, 600)
        self.root.title("JK PasswordManager")
        #self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.iconbitmap("assets\JK.ico")

        container = tk.Frame(self.root)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        LoginHandler(parent=container, controller=self.root)
        db()
    
    #def quit(self):
    #    self.root.destroy()

    
def app_window():
    root = tk.Tk()
    app = JK_Password_Manager(root)
    root.mainloop()

if __name__ == "__main__":
    splash = tk.Tk()
    
    splash_width = 600
    splash_hight = 400
    
    monitor_width = splash.winfo_screenwidth()
    monitor_hight = splash.winfo_screenheight()
    
    x = (monitor_width / 2) - (splash_width / 2)
    y = (monitor_hight / 2) - (splash_hight / 2)
    
    splash.geometry(f"{splash_width}x{splash_hight}+{int(x)}+{int(y)}")
    splash.resizable(False, False)
    splash.overrideredirect(True)
    my_canvas = tk.Canvas(splash)
    my_canvas.pack(fill="both", expand="true")

    def resizer(e):
        global splash_img, resize_image, new_bg
        splash_img = Image.open("assets\loading.png")
        resize_image = splash_img.resize((e.width, e.height), Image.LANCZOS)
        new_bg = ImageTk.PhotoImage(resize_image)
        my_canvas.create_image(0, 0, image=new_bg, anchor="nw")

    splash.bind("<Configure>", resizer)
    splash.after(3000, splash.destroy)
    splash.mainloop()
    app_window()

