import tkinter as tk
from tkinter import filedialog

from integrity_logic import get_file_info, verify_integrity


BG       = "#080B14"
CARD_BG  = "#0E1628"
BORDER   = "#1C2E50"
ACCENT   = "#00D4FF"
ACCENT2  = "#7B5EA7"
BTN_BG   = "#112240"
BTN_HOV  = "#1A3560"
TEXT_PRI = "#E8F4FD"
TEXT_SEC = "#6B8CAE"
SUCCESS  = "#00E5A0"
DANGER   = "#FF4D6D"

file_path     = ""
original_hash = ""

def reset_ui():
    global file_path, original_hash
    file_path     = ""
    original_hash = ""

    file_name_label.config(text="No file selected", fg=TEXT_SEC)
    file_path_label.config(text="")
    file_size_label.config(text="—")
    hash_value_label.config(text="")
    hash_row.pack_forget()

    status_dot.config(fg=TEXT_SEC)
    status_text.config(text="Awaiting file selection…", fg=TEXT_SEC)

    result_frame.pack_forget()
    reset_btn.pack_forget()

    check_btn.config(state="disabled", bg=BTN_BG, fg=TEXT_SEC, cursor="arrow")


def select_file():
    global file_path, original_hash

    path = filedialog.askopenfilename()
    if not path:
        return

    file_path = path
    info      = get_file_info(file_path)
    original_hash = info["hash"]

    file_name_label.config(text=info["name"],        fg=TEXT_PRI)
    file_path_label.config(text=info["short_path"],  fg=TEXT_SEC)
    file_size_label.config(text=info["size_str"],    fg=TEXT_SEC)
    hash_value_label.config(text=info["short_hash"], fg=ACCENT)
    hash_row.pack(pady=(4, 0))

    status_dot.config(fg=ACCENT)
    status_text.config(text="Baseline captured — ready to verify.", fg=TEXT_SEC)

    result_frame.pack_forget()
    reset_btn.pack_forget()

    check_btn.config(state="normal", bg=ACCENT, fg=BG, cursor="hand2")


def check_file():
    if not file_path:
        return

    result = verify_integrity(file_path, original_hash)

    orig_line = f"Original : {result['original_short']}"
    curr_line = f"Current  : {result['current_short']}"

    result_frame.pack(fill="x", padx=24, pady=(0, 6))
    result_frame.config(highlightbackground=SUCCESS if result["intact"] else DANGER)

    if result["intact"]:
        result_icon.config(text="✔",                         fg=SUCCESS)
        result_title.config(text="File is Safe",             fg=SUCCESS)
        result_sub.config(text="Hashes match — unmodified.", fg=TEXT_SEC)
        result_orig.config(text=orig_line,                   fg=TEXT_SEC)
        result_curr.config(text=curr_line,                   fg=SUCCESS)
        status_dot.config(fg=SUCCESS)
        status_text.config(text="Last check: intact",        fg=TEXT_SEC)
    else:
        result_icon.config(text="✖",                            fg=DANGER)
        result_title.config(text="Tampering Detected",          fg=DANGER)
        result_sub.config(text="Hashes differ — file changed.", fg=TEXT_SEC)
        result_orig.config(text=orig_line,                      fg=TEXT_SEC)
        result_curr.config(text=curr_line,                      fg=DANGER)
        status_dot.config(fg=DANGER)
        status_text.config(text="Last check: MODIFIED",         fg=DANGER)

    reset_btn.pack(fill="x", padx=24, pady=(0, 16))

root = tk.Tk()
root.title("File Integrity Checker")
root.geometry("520x640")
root.resizable(False, False)
root.config(bg=BG)

try:
    root.tk.call("tk", "scaling", 1.25)
except Exception:
    pass

header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=28, pady=(28, 0))

tk.Label(header, text="◈  FILE INTEGRITY", bg=BG, fg=ACCENT,
         font=("Courier New", 9, "bold"), anchor="w").pack(side="left")
tk.Label(header, text="SHA-256", bg=BG, fg=TEXT_SEC,
         font=("Courier New", 8), anchor="e").pack(side="right")

tk.Frame(root, bg=BORDER, height=1).pack(fill="x", padx=28, pady=(8, 20))

hero = tk.Frame(root, bg=BG)
hero.pack(padx=28, anchor="w")

tk.Label(hero, text="Integrity\nChecker", bg=BG, fg=TEXT_PRI,
         font=("Georgia", 26, "bold"), justify="left").pack(anchor="w")
tk.Label(hero, text="Detect file tampering with cryptographic hashing.",
         bg=BG, fg=TEXT_SEC, font=("Courier New", 9),
         justify="left").pack(anchor="w", pady=(4, 0))

card = tk.Frame(root, bg=CARD_BG,
                highlightbackground=BORDER, highlightthickness=1,
                padx=18, pady=14)
card.pack(fill="x", padx=24, pady=(20, 0))

row1 = tk.Frame(card, bg=CARD_BG)
row1.pack(fill="x")

tk.Label(row1, text="⬡", bg=CARD_BG, fg=ACCENT2,
         font=("Arial", 18)).pack(side="left", padx=(0, 10))

name_block = tk.Frame(row1, bg=CARD_BG)
name_block.pack(side="left", fill="x", expand=True)

file_name_label = tk.Label(name_block, text="No file selected",
                           bg=CARD_BG, fg=TEXT_SEC,
                           font=("Courier New", 11, "bold"), anchor="w")
file_name_label.pack(anchor="w")

file_path_label = tk.Label(name_block, text="", bg=CARD_BG, fg=TEXT_SEC,
                           font=("Courier New", 8), anchor="w")
file_path_label.pack(anchor="w")

meta_row = tk.Frame(card, bg=CARD_BG)
meta_row.pack(fill="x", pady=(8, 0))

tk.Label(meta_row, text="SIZE", bg=CARD_BG, fg=TEXT_SEC,
         font=("Courier New", 7)).pack(side="left")
file_size_label = tk.Label(meta_row, text="—", bg=CARD_BG, fg=TEXT_SEC,
                           font=("Courier New", 8, "bold"))
file_size_label.pack(side="left", padx=(6, 0))

hash_row = tk.Frame(card, bg=CARD_BG)

tk.Label(hash_row, text="BASELINE", bg=CARD_BG, fg=TEXT_SEC,
         font=("Courier New", 7)).pack(side="left")
hash_value_label = tk.Label(hash_row, text="", bg=CARD_BG, fg=ACCENT,
                            font=("Courier New", 8, "bold"))
hash_value_label.pack(side="left", padx=(6, 0))

btn_row = tk.Frame(root, bg=BG)
btn_row.pack(fill="x", padx=24, pady=(16, 0))

select_btn = tk.Button(btn_row, text="⊕  Select File", command=select_file,
                       bg=BTN_BG, fg=TEXT_PRI,
                       font=("Courier New", 10, "bold"),
                       relief="flat", bd=0, padx=18, pady=10, cursor="hand2",
                       activebackground=BTN_HOV, activeforeground=TEXT_PRI)
select_btn.pack(side="left", padx=(0, 10))
select_btn.bind("<Enter>", lambda e: select_btn.config(bg=BTN_HOV))
select_btn.bind("<Leave>", lambda e: select_btn.config(bg=BTN_BG))

check_btn = tk.Button(btn_row, text="⟳  Check Integrity", command=check_file,
                      bg=BTN_BG, fg=TEXT_SEC,
                      font=("Courier New", 10, "bold"),
                      relief="flat", bd=0, padx=18, pady=10,
                      state="disabled", cursor="arrow",
                      activebackground="#00AACC", activeforeground=BG)
check_btn.pack(side="left")
check_btn.bind("<Enter>",
    lambda e: check_btn.config(bg="#00AACC") if check_btn["state"] == "normal" else None)
check_btn.bind("<Leave>",
    lambda e: check_btn.config(bg=ACCENT)   if check_btn["state"] == "normal" else None)

status_bar = tk.Frame(root, bg=BG)
status_bar.pack(fill="x", padx=24, pady=(12, 0))

status_dot  = tk.Label(status_bar, text="●", bg=BG, fg=TEXT_SEC,
                       font=("Arial", 8))
status_dot.pack(side="left")
status_text = tk.Label(status_bar, text="Awaiting file selection…",
                       bg=BG, fg=TEXT_SEC, font=("Courier New", 8))
status_text.pack(side="left", padx=(5, 0))

result_frame = tk.Frame(root, bg=CARD_BG,
                        highlightbackground=BORDER, highlightthickness=1,
                        padx=20, pady=14)

res_top = tk.Frame(result_frame, bg=CARD_BG)
res_top.pack(anchor="w", fill="x")

result_icon = tk.Label(res_top, text="", bg=CARD_BG, font=("Arial", 22))
result_icon.pack(side="left", padx=(0, 14))

res_text_block = tk.Frame(res_top, bg=CARD_BG)
res_text_block.pack(side="left")

result_title = tk.Label(res_text_block, text="", bg=CARD_BG, fg=TEXT_PRI,
                        font=("Georgia", 13, "bold"), anchor="w")
result_title.pack(anchor="w")

result_sub = tk.Label(res_text_block, text="", bg=CARD_BG, fg=TEXT_SEC,
                      font=("Courier New", 8), anchor="w")
result_sub.pack(anchor="w")

tk.Frame(result_frame, bg=BORDER, height=1).pack(fill="x", pady=(10, 8))

result_orig = tk.Label(result_frame, text="", bg=CARD_BG, fg=TEXT_SEC,
                       font=("Courier New", 8), anchor="w")
result_orig.pack(anchor="w")

result_curr = tk.Label(result_frame, text="", bg=CARD_BG, fg=TEXT_SEC,
                       font=("Courier New", 8, "bold"), anchor="w")
result_curr.pack(anchor="w")

reset_btn = tk.Button(root, text="↺  Reset / Choose New File", command=reset_ui,
                      bg=BTN_BG, fg=TEXT_SEC,
                      font=("Courier New", 9),
                      relief="flat", bd=0, pady=8, cursor="hand2",
                      activebackground=BTN_HOV, activeforeground=TEXT_PRI)
reset_btn.bind("<Enter>", lambda e: reset_btn.config(bg=BTN_HOV, fg=TEXT_PRI))
reset_btn.bind("<Leave>", lambda e: reset_btn.config(bg=BTN_BG,  fg=TEXT_SEC))

tk.Frame(root, bg=BORDER, height=1).pack(side="bottom", fill="x", padx=28)
footer = tk.Frame(root, bg=BG)
footer.pack(side="bottom", fill="x", padx=28, pady=10)

tk.Label(footer,
         text="Algorithm: SHA-256  │  Local Processing  │  Secure Check",
         bg=BG, fg=TEXT_SEC, font=("Courier New", 7)).pack(side="left")

root.mainloop()