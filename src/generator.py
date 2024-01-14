from random import choice
from pyperclip import copy
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os


class PasswordGenerator:
    def __init__(self, root):
        self.generator = tk.Toplevel(root)

        generator_width = 400
        generator_hight = 500

        monitor_width = self.generator.winfo_screenwidth()
        monitor_hight = self.generator.winfo_screenheight()

        x = (monitor_width / 2) - (generator_width / 2)
        y = (monitor_hight / 2) - (generator_hight / 2) - 150

        self.generator.geometry(f"{generator_width}x{generator_hight}+{int(x)}+{int(y)}")
        self.generator.title("JK PasswordGenerator")
        #self.generator.iconbitmap("assets\JK.ico")
        icon_image = tk.PhotoImage(file=os.path.join("assets", "icon.png"))
        self.generator.iconphoto(True, icon_image)
        self.generator.resizable(False, False)
        
        self.generator.focus_force()
        self.generator.grab_set()

        font = ("Arial", 12)

        #ttk.Separator(self.generator, orient="horizontal").pack(fill=X)
        
        Label(self.generator, text="Enter the length of the password:", font=font).pack(fill=X, side=TOP)
        
        self.len_spinbox = Spinbox(self.generator, from_=6, to=64, width=40, font=font,  command=self.get_password)
        self.len_spinbox.delete(0, "end")
        self.len_spinbox.insert(0, 8)
        self.len_spinbox.pack(pady=10)
        
        ttk.Separator(self.generator, orient="horizontal").pack(fill=X, pady=20)
        
        self.options_frame = Frame(self.generator)
        self.options_frame.pack()

        self.letter = BooleanVar(value=True)
        self.letters_checkbox = Checkbutton(self.options_frame, text="Letters", variable=self.letter, font=font, command=self.get_password)
        self.letters_checkbox.grid(row=0, column=0, sticky=W)

        self.digit = BooleanVar(value=True)
        self.digits_checkbox = Checkbutton(self.options_frame, text="Digits", variable=self.digit, font=font, command=self.get_password)
        self.digits_checkbox.grid(row=1, column=0, sticky=W)

        self.symbol = BooleanVar(value=True)
        self.symbols_checkbox = Checkbutton(self.options_frame, text="Symbols", variable=self.symbol, font=font, command=self.get_password)
        self.symbols_checkbox.grid(row=2, column=0, sticky=W)

        ttk.Separator(self.generator, orient="horizontal").pack(fill=X, pady=20)
        
        self.password_entry = Entry(self.generator, width=41, font=font)
        self.password_entry.pack(pady=20)

        self.generate_btn = Button(self.generator, text="Generate Password", font=font, width=20, command=self.get_password)
        self.generate_btn.pack(side=LEFT, padx=10, pady=10)

        self.copy_btn = Button(self.generator, text="Copy Password", font=font, width=20, command=self.copy_password)
        self.copy_btn.pack(side=LEFT, padx=10, pady=10)

        self.get_password()

        self.generator.mainloop()

    def generate(self, length, letters, digits, symbols):
        chars = ""
        
        if letters:
            chars += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if digits:
            chars += "0123456789"
        if symbols:
            chars += '!"' + "#$%&'()*+,-./:;<=>?@[\]^_`{|}~`"

        password = ""
        for i in range(length):
            password += choice(chars)

        return password


    def get_password(self):
        length = int(self.len_spinbox.get())

        letter = self.letter.get()
        digit = self.digit.get()
        symbol = self.symbol.get()

        if not letter and not digit and not symbol:
            messagebox.showerror("Error", "Please check at least one checkbox!")
            return

        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, self.generate(length, letter, digit, symbol))


    def copy_password(self):
        copy(self.password_entry.get())
        messagebox.showinfo("Info", "Password copied successfully!")


#PG = PasswordGenerator()
#PG.run()
