import tkinter as tk 
from handlers.login_handler import LoginHandler
from app_database import database as db_init
from PIL import ImageTk, Image
import requests
import webbrowser
import os, sys
from tkinter import messagebox
import shutil
import time
#from generator import PasswordGenerator


#!######### VERSION #########!#
VERSION = "v6.8"
#!######### VERSION #########!#


def check_version(version):
    url = "https://api.github.com/repos/Josakko/JK_PasswordManager/releases/latest"
    try: res = requests.get(url)
    except: return False, None
    
    if res.status_code == 200:
        res = res.json()
        latest_ver = res["tag_name"]
        if latest_ver != version:
            return res["html_url"], latest_ver
        else:
            return False, None
    else:
        return False, None
    

class JK_Password_Manager:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.minsize(750, 600)
        self.root.title("JK PasswordManager")
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        
        self.root.iconbitmap(os.path.join("assets", "JK.ico"))

        #icon_image = tk.PhotoImage(file=os.path.join("assets", "icon.png"))
        #self.root.iconphoto(True, icon_image)

        container = tk.Frame(self.root)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        LoginHandler(parent=container, root=self.root)
        db_init()
    
    
    def quit(self):
        try: os.mkdir("backups")
        except: pass
        shutil.copy("password_vault.db", os.path.join("backups", f"backup-{time.time()}-password_vault.db"))
        self.root.destroy()

    
def app_window():
    root = tk.Tk()
    app = JK_Password_Manager(root)
    root.mainloop()



def main():
    latest_version = check_version(VERSION)
    if latest_version[0]:
        choice = messagebox.askyesno("Update", f"Looks like new version is available, do you want to update now?\nYour current version is {VERSION} and latest release is {latest_version[1]}.")
        if choice:
            webbrowser.open_new(latest_version[0])


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
        splash_img = Image.open(os.path.join("assets", "loading.png")) #os.path.join("assets", "loading.png")
        resize_image = splash_img.resize((e.width, e.height), Image.LANCZOS)
        new_bg = ImageTk.PhotoImage(resize_image)
        my_canvas.create_image(0, 0, image=new_bg, anchor="nw")


    splash.bind("<Configure>", resizer)
    splash.after(3000, splash.destroy)
    splash.mainloop()
    app_window()




if __name__ == "__main__":
    try:
        main()
    except:
    #except Exception as e:
    #    print(e)
        sys.exit()

