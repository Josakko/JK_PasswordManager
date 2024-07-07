import tkinter as tk
import time
from dialogs.about import About


def bottom_bar(root):
    bottom_frame = tk.Frame(root, relief="raised", borderwidth=3)
    bottom_frame.pack(fill="x", side="bottom")
        
    about_label = tk.Label(bottom_frame, text="About", fg="#007bff", font=("arial", 12, "bold"), cursor="hand2")
    about_label.pack(side="left", padx=15)
        
    about_label.bind("<Button 1>", lambda event: About(root))

    time_label = tk.Label(bottom_frame, font=("arial", 12))
    time_label.pack()

    def tick():
        current_time = time.strftime("%I:%M %p")
        time_label.config(text=current_time)
        time_label.after(200, tick)

    tick()

