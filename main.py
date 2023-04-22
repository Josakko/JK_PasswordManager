import tkinter as tk 
from handlers.login_handler import LoginHandler
from app_database import database as db
from PIL import ImageTk, Image


class Jk_Password_Manager(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.minsize(self, 750, 600)

        self.title("JK PasswordManager")
        self.wm_iconbitmap("Images\\JK.ico")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        LoginHandler(parent=container, controller=self)
        db()
    
def app_window():
    app = Jk_Password_Manager()
    app.mainloop()

if __name__ == "__main__":
    splash = tk.Tk()
    
    splash_width = 600
    splash_hight = 400
    
    monitor_width = splash.winfo_screenwidth()
    monitor_hight = splash.winfo_screenheight()
    
    x = (monitor_width / 2) - (splash_width / 2)
    y = (monitor_hight / 2) - (splash_hight / 2)
    
    splash.geometry(f'{splash_width}x{splash_hight}+{int(x)}+{int(y)}')
    splash.resizable(False, False)
    splash.overrideredirect(True)
    my_canvas = tk.Canvas(splash)
    my_canvas.pack(fill='both', expand='true')

    def resizer(e):
        global splash_img, resize_image, new_bg
        splash_img = Image.open("images\\loading.png")
        resize_image = splash_img.resize((e.width, e.height), Image.ANTIALIAS)
        new_bg = ImageTk.PhotoImage(resize_image)
        my_canvas.create_image(0, 0, image=new_bg, anchor='nw')
    splash.bind("<Configure>", resizer)
    splash.after(3000, splash.destroy)
    splash.mainloop()
    app_window()


#python -m venv venv

#venv\Scripts\activate
#venv\Scripts\deactivate
