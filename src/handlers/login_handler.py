from login import Login


class LoginHandler:
    def __init__(self, parent, root):
        self.par = parent
        self.root = root
        
        self.login_frame()

    def login_frame(self):
        frame = Login(self.par, self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
