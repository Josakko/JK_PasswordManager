import tkinter as tk 
from handlers.login_handler import LoginHandler
from database import Database
from PIL import ImageTk, Image
import os, sys
import shutil
import time
from gui.bottom_bar import bottom_bar
from updater import update

#LANCZOS = 1


def app_window():
    root = tk.Tk()
    root.minsize(750, 600)
    root.title("JK PasswordManager")

    icon = tk.PhotoImage(file=os.path.join("assets", "icon.png"))
    root.iconphoto(True, icon)

    container = tk.Frame(root)
    container.pack(side="top", fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    bottom_bar(root)

    LoginHandler(parent=container, root=root)
    Database().init_db()

    root.mainloop()

def main():
    splash = tk.Tk()
    splash.withdraw()

    splash_width = 600
    splash_hight = 400
    
    monitor_width = splash.winfo_screenwidth()
    monitor_hight = splash.winfo_screenheight()
    
    x = (monitor_width / 2) - (splash_width / 2)
    y = (monitor_hight / 2) - (splash_hight / 2)
    
    splash.geometry(f"{splash_width}x{splash_hight}+{int(x)}+{int(y)}")

    splash.resizable(False, False)
    splash.overrideredirect(True)
    canvas = tk.Canvas(splash)
    canvas.pack(fill="both", expand="true")
    icon = tk.PhotoImage(file=os.path.join("assets", "icon.png"))
    splash.iconphoto(True, icon)

    update()

    splash.deiconify()


    def resizer(event):
        global splash_img, resize_image, new_bg
        splash_img = Image.open(os.path.join("assets", "loading.png"))
        resize_image = splash_img.resize((event.width, event.height), Image.LANCZOS)
        new_bg = ImageTk.PhotoImage(resize_image)
        canvas.create_image(0, 0, image=new_bg, anchor="nw")


    splash.bind("<Configure>", resizer)
    splash.after(3000, splash.destroy)
    splash.mainloop()

    app_window()


if __name__ == "__main__":
    try:
        main()
    #except:
    except Exception as e:
        print(e)
        pass

    try: os.mkdir("backups")
    except: pass
    try: shutil.copy("password_vault.db", os.path.join("backups", f"backup-{time.time()}-password_vault.db"))
    except: pass

    sys.exit()

# TODO
# add better version checking
# TODO
