import tkinter as tk
import time
from tkinter import ttk, font, filedialog
import pyperclip
from app_database import insert
from app_database import update
from app_database import delete
from app_database import delete_user_data
from app_database import get_password
from generator import PasswordGenerator
import tkinter.messagebox as msg
from handlers import login_handler
import webbrowser 
import csv
import os



class Dashboard(tk.Frame):
    def __init__(self, parent, root, user_id, user_name, data, f):
        tk.Frame.__init__(self, parent, bg="#3d3d5c")
        self.root = root
        self.user_id = user_id
        self.user_name = user_name
        self.data = data
        self.f = f

        heading_frame = tk.Frame(self, bg="#33334d")
        tk.Label(heading_frame, text="User Name : ", font=("arial", 13), fg="white", bg="#33334d").pack(padx=10, side="left")
        tk.Label(heading_frame, text=self.user_name, font=("arial", 13), fg="white", bg="#33334d").pack(side="left")
        tk.Label(heading_frame, text=" " * 20, bg="#33334d").pack(padx=10, side="left")
        tk.Label(heading_frame, text="Total: ", font=("arial", 13), fg="white", bg="#33334d", ).pack(side="left")
        total_entries = tk.Label(heading_frame, text=len(self.data), font=("arial", 13), fg="white", bg="#33334d", )
        total_entries.pack(side="left")

        def logout():
            login_handler.LoginHandler(parent, self.root)
            
        logout_button = tk.Button(heading_frame, text="LOGOUT", command=logout, width=15, relief="raised")
        logout_button.pack(padx=10, side="right")

        heading_frame.pack(fill="x", pady=10)

        def copy_menu(event):
            item = data_tree.identify("item", event.x, event.y)
            column = data_tree.identify("column", event.x, event.y)
            
            if item and column:
                def copy():
                    if column == "#0": 
                        text = data_tree.item(item, "text")
                        name = "Platform"
                    elif column == "#4":
                        msg.showerror("Error", 'Please use "Copy Password" button in order to copy password!'); return
                    else: 
                        text = data_tree.set(item, column)
                        name = data_tree.heading(column)["text"]

                    pyperclip.copy(text)
                    msg.showinfo("Info", f"{name} copied to clipboard!")


                menu = tk.Menu(table_frame, tearoff=0)
                menu.add_command(label="Copy", command=copy)
                menu.post(event.x_root, event.y_root)


        def deselect(event):
            data_tree.selection_remove(data_tree.focus())
        
        
        table_frame = tk.Frame(self)
        tree_scroll = tk.Scrollbar(table_frame)
        tree_scroll.pack(side="right", fill="y")
        data_tree = ttk.Treeview(table_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        data_tree.bind("<Button-1>", deselect)
        data_tree.bind("<Button-3>", copy_menu)
        tree_scroll.config(command=data_tree.yview)

        data_tree["columns"] = ("S.No", "Platform", "Username", "Password", "Time")
        data_tree.column("#0", width=0, stretch="no")
        data_tree.column("S.No", anchor="w", width=0)
        data_tree.column("Platform", anchor="center", width=30)
        data_tree.column("Username", anchor="center", width=30)
        data_tree.column("Password", anchor="center", width=30)
        data_tree.column("Time", anchor="center", width=30)

        data_tree.heading("#0", text="Label", anchor="w")
        data_tree.heading("S.No", text="S.No", anchor="w")
        data_tree.heading("Platform", text="Platform", anchor="center")
        data_tree.heading("Username", text="Username", anchor="center")
        data_tree.heading("Password", text="Password", anchor="center")
        data_tree.heading("Time", text="Time", anchor="center")

        global count
        count = 0
        for record in self.data:
            display_password = "*"*len(record[3])
            count += 1
            data_tree.insert(parent="", index="end", iid=record[0], text="", values=(count, record[1], record[2], display_password, record[4]))

        data_tree.pack(fill="both", expand="True")
        table_frame.pack(fill="both", expand="True")

        button_frame1 = tk.Frame(self, relief="raised", bg="#3d3d5c")
        button_frame1.pack(pady=10)

        tk.Label(button_frame1, text="Platform", fg="white", bg="#3d3d5c").grid(row=0, column=0)
        tk.Label(button_frame1, text="Username", fg="white", bg="#3d3d5c").grid(row=0, column=1)
        tk.Label(button_frame1, text="Password", fg="white", bg="#3d3d5c").grid(row=0, column=2)
        add_update_platform = tk.Entry(button_frame1, textvariable="add_update_platform", font=13)
        add_update_platform.grid(row=1, column=0)
        add_update_username = tk.Entry(button_frame1, textvariable="add_update_username", font=13)
        add_update_username.grid(row=1, column=1)
        add_update_password = tk.Entry(button_frame1, textvariable="add_update_password", font=13)
        add_update_password.grid(row=1, column=2)


        def update_row(row_id, platform, username, password, time_stamp=time.strftime("%I:%M %p %d-%m-%Y")):
            #time_stamp = time.strftime("%I:%M %p %d-%m-%Y")

            row = [platform, username, password, time_stamp, self.user_id, row_id]
            update(row, self.f)
            serial_number = data_tree.item(row_id, "values")[0]
            display_password = "*" * len(password)
            data_tree.item(row_id, text="", values=(serial_number, platform, username, display_password, time_stamp))

        def insert_row(platform, username, password, time_stamp=time.strftime("%I:%M %p %d-%m-%Y")):
            #time_stamp = time.strftime("%I:%M %p %d-%m-%Y")
            global count

            row = [platform, username, password, time_stamp, self.user_id]
            new_id = insert(row, self.f)
            display_password = "*"*len(password)
            count += 1
            data_tree.insert(parent="", index="end", iid=new_id, text="", values=(count, platform, username, display_password, time_stamp))
            total_entries["text"] = count
                
        def add_update_row():
            if not add_update_platform.get() and not add_update_username.get() and not add_update_password.get():
                msg.showerror("Error", "Fill out at least one field!")
                return

            selected = data_tree.focus()
            if data_tree.selection():
                decision = msg.askokcancel("Warning", "Are you sure you want to update selected row?")
                if decision:
                    update_row(selected, add_update_platform.get(), add_update_username.get(), add_update_password.get())
                else:
                    return
            else:
                insert_row(add_update_platform.get(), add_update_username.get(), add_update_password.get())

            add_update_platform.delete(0, "end")
            add_update_username.delete(0, "end")
            add_update_password.delete(0, "end")

        add_button = tk.Button(button_frame1, command=add_update_row, text="Add / Update", width=20, relief="raised")
        add_button.grid(row=1, column=3, padx=20)


        button_frame = tk.Frame(self, relief="raised", bg="#33334d")
        button_frame.pack(fill="x", pady=30)
        

        def delete_row():
            if data_tree.selection():
                decision = msg.askokcancel("Warning", "Are you sure you want to delete selected password ?")
                if decision:
                    x = data_tree.selection()
                else:
                    return
                delete(x)
                global count
                if len(x) == 1:
                    data_tree.delete(x)
                    count -= 1
                else:
                    for i in x:
                        data_tree.delete(i)
                        count -= 1
                total_entries["text"] = count
            else:
                msg.showerror("ERROR", "Please select one above!")
            
        delete_button = tk.Button(button_frame, text="Delete",bg="red", command=delete_row, relief="raised", width=10)
        delete_button.pack(pady=10, padx=10, side="left")
        

        def copy_password():
            if data_tree.selection():
                selected_password = get_password(data_tree.focus(), self.user_id, self.f)
                pyperclip.copy(selected_password)
                msg.showinfo("Info", "Password copied.")
            else:
                msg.showerror("ERROR", "Please select one above!")
                
        copy_button = tk.Button(button_frame, text="Copy Password", command=copy_password, relief="raised", width=15)
        copy_button.pack(pady=10, padx=15, side="left")


        def show_password():
            if data_tree.selection():
                selected_password = get_password(data_tree.focus(), self.user_id, self.f)
                selected_row_data = data_tree.item(data_tree.focus(), "values")
                msg.showinfo("Login Credentials", f'Your password for "{selected_row_data[1]}" is "{selected_password}" and username is "{selected_row_data[2]}".')
            else:
                msg.showerror("ERROR", "Please select one above!")
                
        show_button = tk.Button(button_frame, text="Show Password", command=show_password, relief="raised", width=15)
        show_button.pack(pady=10, padx=15, side="left")


        def run_password_generator():
            PasswordGenerator(self)
           
        password_generator_btn = tk.Button(button_frame, text="Password Generator", width=15, relief="raised", command=run_password_generator)
        password_generator_btn.pack(pady=10, padx=15, side="left")
        

        def delete_all_row():
            decision = msg.askokcancel("Warning", "Are you sure to delete all ?")
            if decision:
                delete_user_data(self.user_id)
                for x in data_tree.get_children():
                    data_tree.delete(x)
                global count
                count = 0
                total_entries["text"] = 0

        delete_all_button = tk.Button(button_frame, text="Delete All Passwords", command=delete_all_row, relief="raised", bg="red", width=20)
        delete_all_button.pack(pady=10, padx=50, side="right")


        def get_data():
            data = []

            for id in data_tree.get_children():
                values = data_tree.item(id, "values")
                password = get_password(id, self.user_id, self.f)
                row = (values[1], values[2], password, values[4])
                data.append(row)

            return data
        
        def write(file):
            try:
                with open(file, "w", newline="", encoding="utf-8") as export_f:
                    f = csv.writer(export_f)
                    f.writerows(get_data())
                
                msg.showinfo("Export", f"Successfully exported passwords to {file}!")
            except:
                msg.showerror("Error", "Invalid path!")
        
        def export():
            msg.showwarning("Warning", "If you continue all stored credentials will be exported in unprotected plain text and will be exposed to danger of being stolen!")
            
            file = filedialog.asksaveasfilename(title="Export", initialfile="export.csv", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            
            if not file:
                return

            write(file)
            
        export_button = tk.Button(button_frame, text="Export to CSV", command=export, relief="raised", width=15)
        export_button.pack(pady=10, padx=15, side="right")
        

        def read(file):
            try:
                with open(file, "r", encoding="utf-8") as import_f:
                    data = csv.reader(import_f)

                    for row in data:
                        insert_row(row[0], row[1], row[2], time.strftime("%I:%M %p %d-%m-%Y") if not row[3] else row[3])
                        
                msg.showinfo("Import", f"Successfully imported passwords from {file}!")
            except:
                msg.showerror("Error", "Invalid file format or csv format!")
                return

        def import_():
            file = filedialog.askopenfilename(title="Import", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if not file: return

            if os.path.isfile(file):
                read(file)
                
            else:
                msg.showerror("Error", "Invalid file path!")
                return
            
        import_button = tk.Button(button_frame, text="Import from CSV", command=import_, relief="raised", width=15)
        import_button.pack(pady=10, padx=15, side="right")


        def about():
            about = tk.Toplevel(self)
            about.title("About - JK PasswordManager")

            window_width = 600
            window_hight = 200

            monitor_width = about.winfo_screenwidth()
            monitor_hight = about.winfo_screenheight()

            x = (monitor_width / 2) - (window_width / 2)
            y = (monitor_hight / 2) - (window_hight / 2)

            about.geometry(f"{window_width}x{window_hight}+{int(x)}+{int(y)}")
            icon_image = tk.PhotoImage(file=os.path.join("assets", "icon.png"))
            about.iconphoto(True, icon_image)
            about.configure(bg="#f5f5f5")
            about.resizable(False, False)
            about.focus_force()
            # about.grab_set()

            custom_font = font.Font(family="Helvetica", size=12, weight="bold")

            frame = tk.Frame(about, bg="#f5f5f5")
            frame.pack(pady=50)

            text = "JK PasswordManager is an open source app created by Josakko, \nall documentation and instructions can be found on"
            label_text = tk.Label(frame, text=text, font=custom_font, bg="#f5f5f5", fg="#333333")
            label_text.pack(side=tk.LEFT)

            link_text = tk.Label(frame, text="GitHub", font=custom_font, bg="#f5f5f5", fg="#007bff", cursor="hand2")
            link_text.pack(side=tk.LEFT, anchor="sw") #side=tk.BOTTOM

            def open_link(event):
                webbrowser.open_new("https://github.com/Josakko/JK_PasswordManager")

            link_text.bind("<Button-1>", open_link)

            
        bottom_frame = tk.Frame(self, relief="raised", borderwidth=3)
        bottom_frame.pack(fill="x", side="bottom")
        
        
        about_label = tk.Label(bottom_frame, text="About", fg="#007bff", font=("arial", 12, "bold"), cursor="hand2")
        about_label.pack(side="left", padx=15)
        
        about_label.bind("<Button 1>", lambda event: about())


        def tick():
            current_time = time.strftime("%I:%M %p")
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=("arial", 12))
        time_label.pack()
        tick()

        
