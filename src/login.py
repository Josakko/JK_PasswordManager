import tkinter as tk  
from database import Database
from handlers.dashboard_handler import DashboardHandler
from utils import decrypt_credentials
from dialogs.register import Register


class Login(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent, bg="#3d3d5c")
        self.root: tk.Tk = root
        self.parent: tk.Frame = parent
        self.root.wm_state("normal") #! zoomed is windows only other options - normal, icon, iconic, withdrawn
        self.db = Database()

        tk.Label(self, text="JK Password Manager", font=("arial", 45, "bold"), foreground="white", background="#3d3d5c").pack(pady=25)
        tk.Label(self, height=4, bg="#3d3d5c").pack()
        tk.Label(self, text="Enter your username", font=("arial", 13), fg="white", bg="#3d3d5c").pack(pady=10)

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.username_entry_box = tk.Entry(self, textvariable=self.username, font=("arial", 12), width=22)
        self.username_entry_box.focus_set()
        self.username_entry_box.pack(ipady=7)

        tk.Label(self, text="Enter your password", font=("arial", 13), fg="white", bg="#3d3d5c").pack(pady=10)

        self.password_entry_box = tk.Entry(self, textvariable=self.password, font=("arial", 12), width=22)
        self.password_entry_box.pack(ipady=7)

        self.password_entry_box.bind("<FocusIn>", self.handle_focus_in)
        self.password_entry_box.bind("<Return>", self.on_enter_press)
        self.username_entry_box.bind("<Return>", self.on_enter_press)

        self.enter_button = tk.Button(self, text="Login", font=("arial", 13), command=self.check_password, relief="raised", borderwidth=3, height=2, width=15)
        self.enter_button.pack(pady=20)

        control_frame = tk.Frame(self, relief="raised", bg="#33334d")
        control_frame.pack(fill="both", expand=True)

        self.incorrect_password_label = tk.Label(control_frame, text="", font=("arial", 13), fg="#ff0000", bg="#33334d", anchor="n")
        self.incorrect_password_label.pack(pady=10)

        sign_up_btn = tk.Button(control_frame, text="Sign Up", command=lambda: Register(self), relief="raised", bg="#3d3d5c", font=("arial", 13), fg="white")
        sign_up_btn.pack(pady=5)


    def on_enter_press(self, event: tk.Event):
        if self.username.get() != "":
            if self.password.get() != "":
                self.enter_button.invoke()

            else:
                self.password_entry_box.focus()

        elif self.password.get() != "":
            self.username_entry_box.focus()
            

    def handle_focus_in(self, _):
        self.password_entry_box.configure(fg="black", show="*")


    def check_password(self):
        if not self.username.get():
            self.incorrect_password_label["text"] = "Invalid Username"
            return
        
        if not self.password.get():
            self.incorrect_password_label["text"] = "Invalid Password"            

        response = self.db.login(self.username.get(), self.password.get())
        if not response:
            self.password.set("")
            self.incorrect_password_label["text"] = "Incorrect Username and Password"
            return
        
        user_id, username, encrypted_data, f = response[0], response[1], response[2], response[3]
        data = decrypt_credentials(encrypted_data, f)

        self.incorrect_password_label["text"] = ""

        self.username.set("")
        self.password.set("")

        DashboardHandler(self.parent, self.root, user_id, username, data, self.db)
        self.destroy()
