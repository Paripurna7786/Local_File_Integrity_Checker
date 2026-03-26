import hashlib
import tkinter as tk
from tkinter import filedialog


bg_color = "#0D0630"
btn_color = "#384E77"
text_color = "#E6F9AF"

file_path = ""
original_hash = ""

def get_hash(filename):
    with open(filename, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def select_file():
    global file_path, original_hash
    file_path = filedialog.askopenfilename()
    if file_path:
        original_hash = get_hash(file_path)
        file_label.config(text="File Selected", fg="lightgreen")

def check_file():
    if not file_path:
        result_label.config(text="Select file first!", fg="red")
        return

    new_hash = get_hash(file_path)

    if new_hash == original_hash:
        result_label.config(text="✔ File NOT changed", fg="lightgreen")
    else:
        result_label.config(text="✖ File MODIFIED", fg="red")

root = tk.Tk()
root.title("File Integrity Checker")
root.geometry("500x300")
root.config(bg=bg_color)

title = tk.Label(root, text="File Integrity Checker",
                 bg=bg_color, fg=text_color,
                 font=("Arial", 18, "bold"))
title.pack(pady=15)

select_btn = tk.Button(root, text="Select File",
                       command=select_file,
                       bg=btn_color, fg="white",
                       font=("Arial", 12), padx=10, pady=5)
select_btn.pack(pady=10)


file_label = tk.Label(root, text="No file selected",
                      bg=bg_color, fg="white",
                      font=("Arial", 10))
file_label.pack()


check_btn = tk.Button(root, text="Check Integrity",
                      command=check_file,
                      bg=btn_color, fg="white",
                      font=("Arial", 12), padx=10, pady=5)
check_btn.pack(pady=15)


result_label = tk.Label(root, text="",
                        bg=bg_color,
                        font=("Arial", 14, "bold"))
result_label.pack(pady=10)

root.mainloop()