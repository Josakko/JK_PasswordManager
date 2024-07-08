import tkinter as tk
import tkinter.messagebox as msg
import os
from database import Database

class Register:
    def __init__(self, root):
        self.reg = tk.Toplevel(root)
        
        window_width = 400
        window_hight = 400

        monitor_width = self.reg.winfo_screenwidth()
        monitor_hight = self.reg.winfo_screenheight()

        x = (monitor_width / 2) - (window_width / 2)
        y = (monitor_hight / 2) - (window_hight / 2)

        self.reg.geometry(f"{window_width}x{window_hight}+{int(x)}+{int(y)}")
        self.reg.title("Sign Up")
        self.reg.config(bg="#3d3d5c")

        icon_image = tk.PhotoImage(file=os.path.join("assets", "icon.png"))
        self.reg.iconphoto(True, icon_image)
        self.reg.resizable(width=False, height=False)
        self.reg.focus_force()
        self.reg.grab_set()

        tk.Label(self.reg, text="Enter your username", font=("arial", 13), fg="white", bg="#3d3d5c").pack(pady=10)

        self.new_username = tk.StringVar()
        self.new_password = tk.StringVar()
        self.confirm_password = tk.StringVar()
        self.new_username_entry_box = tk.Entry(self.reg, textvariable=self.new_username, font=("arial", 12), width=22)
        self.new_username_entry_box.focus_set()
        self.new_username_entry_box.pack(ipady=7)

        tk.Label(self.reg, text="Enter your password", font=("arial", 13), fg="white", bg="#3d3d5c").pack(pady=10)

        self.new_password_entry_box = tk.Entry(self.reg, textvariable=self.new_password, font=("arial", 12), width=22)
        self.new_password_entry_box.pack(ipady=7)

        tk.Label(self.reg, text="Confirm your password", font=("arial", 13), fg="white", bg="#3d3d5c").pack(pady=10)

        self.confirm_password_entry_box = tk.Entry(self.reg, textvariable=self.confirm_password, font=("arial", 12), width=22)
        self.confirm_password_entry_box.pack(ipady=7)

        self.new_password_entry_box.bind("<FocusIn>", self.handle_focus_in)
        self.confirm_password_entry_box.bind("<FocusIn>", self.handle_focus_in)

        self.new_username_entry_box.bind("<Return>", self.on_enter_press)
        self.new_password_entry_box.bind("<Return>", self.on_enter_press)
        self.confirm_password_entry_box.bind("<Return>", self.on_enter_press)

        self.register_button = tk.Button(self.reg, text="Register", font=("arial", 13), relief="raised", command=self.register, borderwidth=3, height=2, width=15)
        self.register_button.pack(pady=20)

        self.incorrect_info_label = tk.Label(self.reg, text="", font=("arial", 13), fg="#ff0000", bg="#3d3d5c", anchor="n")
        self.incorrect_info_label.pack(pady=10)


    def on_enter_press(self, event: tk.Event):
        if self.new_username.get() != "":
            if self.new_password.get() != "":
                if self.confirm_password.get() != "":
                    self.register_button.invoke()
                else:
                    self.confirm_password_entry_box.focus_set()
            else:
                self.new_password_entry_box.focus_set()

        elif self.new_password.get() != "":
            self.new_username_entry_box.focus_set()

        elif self.confirm_password.get() != "":
            self.new_username_entry_box.focus_set()


    def register(self):
        if not self.new_username.get():
            self.incorrect_info_label["text"] = "Please enter username."
            return

        if self.new_password.get() != self.confirm_password.get():
            self.incorrect_info_label["text"] = "Passwords do not match!"
            return

        if len(self.new_password.get()) < 6:
            self.incorrect_info_label["text"] = "This password is too short, minimum is 6."
            return
        
        if not Database().register(self.new_username.get(), self.new_password.get()):
            self.incorrect_info_label["text"] = "This username already exist."
            return
        
        self.reg.destroy()
        msg.showinfo("Register", "Your registration successful!")
        msg.showwarning("Warning", "Make sure to save this master password since if lost all credentials saved on this account are permanently lost and cant be recovered without original password!")


    def handle_focus_in(self, _):
        self.new_password_entry_box.configure(fg="black", show="*")
        self.confirm_password_entry_box.configure(fg="black", show="*")

    