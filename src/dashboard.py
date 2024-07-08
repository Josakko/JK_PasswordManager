import tkinter as tk
import time
from tkinter import ttk, filedialog
import pyperclip
from database import Database
from dialogs.generator import PasswordGenerator
import tkinter.messagebox as msg
from handlers import login_handler
import csv
import os


class Dashboard(tk.Frame):
    def __init__(self, parent, root, user_id, user_name, data, db):
        tk.Frame.__init__(self, parent, bg="#3d3d5c")
        self.root = root
        self.parent = parent
        self.user_id = user_id
        self.user_name = user_name
        self.data = data
        self.db: Database = db

        heading_frame = tk.Frame(self, bg="#33334d")
        tk.Label(heading_frame, text="User Name : ", font=("arial", 13), fg="white", bg="#33334d").pack(padx=10, side="left")
        tk.Label(heading_frame, text=self.user_name, font=("arial", 13), fg="white", bg="#33334d").pack(side="left")
        tk.Label(heading_frame, text=" " * 20, bg="#33334d").pack(padx=10, side="left")
        tk.Label(heading_frame, text="Total: ", font=("arial", 13), fg="white", bg="#33334d", ).pack(side="left")
        self.total_entries = tk.Label(heading_frame, text=len(self.data), font=("arial", 13), fg="white", bg="#33334d", )
        self.total_entries.pack(side="left")

        logout_button = tk.Button(heading_frame, text="LOGOUT", command=self.logout, width=15, relief="raised")
        logout_button.pack(padx=10, side="right")

        heading_frame.pack(fill="x", pady=10)

        self.table_frame = tk.Frame(self)
        tree_scroll = tk.Scrollbar(self.table_frame)
        tree_scroll.pack(side="right", fill="y")
        self.data_tree = ttk.Treeview(self.table_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        self.data_tree.bind("<Button-1>", self.deselect)
        self.data_tree.bind("<Button-3>", self.copy_menu)
        tree_scroll.config(command=self.data_tree.yview)

        self.data_tree["columns"] = ("S.No", "Platform", "Username", "Password", "Time")
        self.data_tree.column("#0", width=0, stretch="no")
        self.data_tree.column("S.No", anchor="w", width=0)
        self.data_tree.column("Platform", anchor="center", width=30)
        self.data_tree.column("Username", anchor="center", width=30)
        self.data_tree.column("Password", anchor="center", width=30)
        self.data_tree.column("Time", anchor="center", width=30)

        self.data_tree.heading("#0", text="Label", anchor="w")
        self.data_tree.heading("S.No", text="S.No", anchor="w")
        self.data_tree.heading("Platform", text="Platform", anchor="center")
        self.data_tree.heading("Username", text="Username", anchor="center")
        self.data_tree.heading("Password", text="Password", anchor="center")
        self.data_tree.heading("Time", text="Time", anchor="center")

        self.count = 0
        for record in self.data:
            display_password = "*" * len(record[3])
            self.count += 1
            self.data_tree.insert(parent="", index="end", iid=record[0], text="", values=(self.count, record[1], record[2], display_password, record[4]))

        self.data_tree.pack(fill="both", expand="True")
        self.table_frame.pack(fill="both", expand="True")

        button_frame1 = tk.Frame(self, relief="raised", bg="#3d3d5c")
        button_frame1.pack(pady=10)

        tk.Label(button_frame1, text="Platform", fg="white", bg="#3d3d5c").grid(row=0, column=0)
        tk.Label(button_frame1, text="Username", fg="white", bg="#3d3d5c").grid(row=0, column=1)
        tk.Label(button_frame1, text="Password", fg="white", bg="#3d3d5c").grid(row=0, column=2)
        self.add_update_platform = tk.Entry(button_frame1, textvariable="add_update_platform", font=13)
        self.add_update_platform.grid(row=1, column=0)
        self.add_update_username = tk.Entry(button_frame1, textvariable="add_update_username", font=13)
        self.add_update_username.grid(row=1, column=1)
        self.add_update_password = tk.Entry(button_frame1, textvariable="add_update_password", font=13)
        self.add_update_password.grid(row=1, column=2)

        self.add_update_platform.bind("<Return>", self.on_enter_press)
        self.add_update_username.bind("<Return>", self.on_enter_press)
        self.add_update_password.bind("<Return>", self.on_enter_press)

        self.add_button = tk.Button(button_frame1, command=self.add_update_row, text="Add / Update", width=20, relief="raised")
        self.add_button.grid(row=1, column=3, padx=20)

        button_frame = tk.Frame(self, relief="raised", bg="#33334d")
        button_frame.pack(fill="x", pady=30)
            
        delete_button = tk.Button(button_frame, text="Delete",bg="red", command=self.delete_row, relief="raised", width=10)
        delete_button.pack(pady=10, padx=10, side="left")
        
        copy_button = tk.Button(button_frame, text="Copy Password", command=self.copy_password, relief="raised", width=15)
        copy_button.pack(pady=10, padx=15, side="left")

        show_button = tk.Button(button_frame, text="Show Password", command=self.show_password, relief="raised", width=15)
        show_button.pack(pady=10, padx=15, side="left")
  

        password_generator_btn = tk.Button(
                                    button_frame, 
                                    text="Password Generator", 
                                    width=15, relief="raised", 
                                    command=lambda: PasswordGenerator(self) )
        password_generator_btn.pack(pady=10, padx=15, side="left")
        
        delete_all_button = tk.Button(button_frame, text="Delete All Passwords", command=self.delete_all_rows, relief="raised", bg="red", width=20)
        delete_all_button.pack(pady=10, padx=50, side="right")


        export_button = tk.Button(button_frame, text="Export to CSV", command=self.export, relief="raised", width=15)
        export_button.pack(pady=10, padx=15, side="right")
        
        import_button = tk.Button(button_frame, text="Import from CSV", command=self.import_, relief="raised", width=15)
        import_button.pack(pady=10, padx=15, side="right")

        self.cp_menu = tk.Menu(self.table_frame, tearoff=0)


    def logout(self):
        login_handler.LoginHandler(self.parent, self.root)
        self.destroy()

    def copy_menu(self, event: tk.Event):
        item = self.data_tree.identify("item", event.x, event.y)
        column = self.data_tree.identify("column", event.x, event.y)

        if not item or not column:
            return
        
        def copy():
            if column == "#0": 
                text = self.data_tree.item(item, "text")
                name = "Platform"
            elif column == "#4":
                msg.showerror("Error", 'Please use "Copy Password" button in order to copy password!'); return
            else: 
                text = self.data_tree.set(item, column)
                name = self.data_tree.heading(column)["text"]

            pyperclip.copy(text)
            msg.showinfo("Info", f"{name} copied to clipboard!")
        
        self.cp_menu.unpost()
        self.cp_menu.delete(0, tk.END)
        self.cp_menu.add_command(label="Copy", command=copy)
        self.cp_menu.post(event.x_root, event.y_root)


    def deselect(self, event: tk.Event):
        self.data_tree.selection_remove(self.data_tree.focus())
        self.cp_menu.unpost()


    def update_row(self, row_id, platform, username, password, time_stamp=time.strftime("%I:%M %p %d-%m-%Y")):
        row = [platform, username, password, time_stamp, self.user_id, row_id]
        self.db.update(row)
        serial_number = self.data_tree.item(row_id, "values")[0]
        display_password = "*" * len(password)
        self.data_tree.item(row_id, text="", values=(serial_number, platform, username, display_password, time_stamp))


    def insert_row(self, platform, username, password, time_stamp=time.strftime("%I:%M %p %d-%m-%Y")):
        row = [platform, username, password, time_stamp, self.user_id]
        new_id = self.db.insert(row)
        display_password = "*" * len(password)
        self.count += 1
        self.data_tree.insert(parent="", index="end", iid=new_id, text="", values=(self.count, platform, username, display_password, time_stamp))
        self.total_entries["text"] = self.count
            

    def add_update_row(self):
        if not self.add_update_platform.get() and not self.add_update_username.get() and not self.add_update_password.get():
            msg.showerror("Error", "Fill out at least one field!")
            return

        selected = self.data_tree.focus()
        if not self.data_tree.selection():
            self.insert_row(self.add_update_platform.get(), self.add_update_username.get(), self.add_update_password.get())
        
        elif msg.askokcancel("Warning", "Are you sure you want to update selected row?"):
            self.update_row(selected, self.add_update_platform.get(), self.add_update_username.get(), self.add_update_password.get())

        else: return

        self.add_update_platform.delete(0, "end")
        self.add_update_username.delete(0, "end")
        self.add_update_password.delete(0, "end")


    def delete_row(self):
        if not self.data_tree.selection():
            msg.showerror("ERROR", "Please select one above!")
            return
        
        decision = msg.askokcancel("Warning", "Are you sure you want to delete selected password ?")
        if not decision:
            return
        
        rows = self.data_tree.selection()
        self.db.delete(rows)

        if len(rows) == 1:
            self.data_tree.delete(rows)
            self.count -= 1
            return

        for row in rows:
            self.data_tree.delete(row)
            self.count -= 1
        self.total_entries["text"] = self.count


    def copy_password(self):
        if not self.data_tree.selection():
            msg.showerror("ERROR", "Please select one above!")
            return

        selected_password = self.db.get_password(self.data_tree.focus(), self.user_id)
        pyperclip.copy(selected_password)
        msg.showinfo("Info", "Password copied.")


    def show_password(self):
        if not self.data_tree.selection():
            msg.showerror("ERROR", "Please select one above!")
            return

        selected_password = self.db.get_password(self.data_tree.focus(), self.user_id)
        selected_row_data = self.data_tree.item(self.data_tree.focus(), "values")
        msg.showinfo("Login Credentials", f'Your password for "{selected_row_data[1]}" is "{selected_password}" and username is "{selected_row_data[2]}".')


    def delete_all_rows(self):
        decision = msg.askokcancel("Warning", "Are you sure to delete all ?")
        if not decision:
            return
        
        self.db.delete_user_data(self.user_id)
        for x in self.data_tree.get_children():
            self.data_tree.delete(x)

        self.count = 0
        self.total_entries["text"] = 0


    def get_data(self):
        data = []

        for id in self.data_tree.get_children():
            values = self.data_tree.item(id, "values")
            password = self.db.get_password(id, self.user_id)
            row = (values[1], values[2], password, values[4])
            data.append(row)

        return data
        

    def write(self, file):
        try:
            with open(file, "w", newline="", encoding="utf-8") as export_f:
                f = csv.writer(export_f)
                f.writerows(self.get_data())
            
            msg.showinfo("Export", f"Successfully exported passwords to {file}!")
        except:
            msg.showerror("Error", "Invalid path!")
        

    def export(self):
        msg.showwarning("Warning", "If you continue all stored credentials will be exported in unprotected plain text and will be exposed to danger of being stolen!")
        
        file = filedialog.asksaveasfilename(title="Export", initialfile="export.csv", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        
        if not file:
            return
        
        self.write(file)


    def read(self, file):
        try:
            with open(file, "r", encoding="utf-8") as import_f:
                data = csv.reader(import_f)

                for row in data:
                    self.insert_row(row[0], row[1], row[2], time.strftime("%I:%M %p %d-%m-%Y") if not row[3] else row[3])
                    
            msg.showinfo("Import", f"Successfully imported passwords from {file}!")
        except:
            msg.showerror("Error", "Invalid file format or csv format!")
            return
        

    def import_(self):
        file = filedialog.askopenfilename(title="Import", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not file: return

        if not os.path.isfile(file):
            msg.showerror("Error", "Invalid file path!")
            return
        
        self.read(file)


    def on_enter_press(self, event: tk.Event):
        focus_widget = self.focus_get()
        if focus_widget == self.add_update_platform:
            self.add_update_username.focus_set()
        
        elif focus_widget == self.add_update_username:
            self.add_update_password.focus_set()
        
        elif focus_widget == self.add_update_password:
            self.add_button.invoke()
