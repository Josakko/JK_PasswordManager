from dashboard import Dashboard


class DashboardHandler:
    def __init__(self, parent, controller, user_id, user_name, data, f):
        self.par = parent
        self.con = controller
        self.user_id = user_id
        self.user_name = user_name
        self.data = data
        self.f = f
        
        self.dashboard_frame()

    def dashboard_frame(self):
        frame = Dashboard(self.par, self.con, self.user_id, self.user_name, self.data, self.f)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
