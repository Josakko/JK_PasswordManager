from dashboard import Dashboard


class DashboardHandler:
    def __init__(self, parent, root, user_id: str, user_name: str, data: list, db):
        self.par = parent
        self.root = root
        self.user_id = user_id
        self.user_name = user_name
        self.data = data
        self.db = db
        
        self.dashboard_frame()

    def dashboard_frame(self):
        frame = Dashboard(self.par, self.root, self.user_id, self.user_name, self.data, self.db)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
