"""
Safe in-app key-event logger (educational).
Logs key presses only while the tkinter window is focused.
Saves timestamped entries to 'key_log.txt'.
"""

import tkinter as tk
from datetime import datetime
import os

LOG_FILE = "key_log.txt"

def log_key(event):
    """
    Called on key press while window has focus.
    event.keysym is the symbolic name (e.g., 'a', 'Return', 'Shift_L').
    """
    timestamp = datetime.utcnow().isoformat() + "Z"  # UTC ISO timestamp
    entry = f"{timestamp}\t{event.keysym}\tchar:{repr(event.char)}\n"
    # Append to log file
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
    # Optionally show in the UI for immediate feedback
    status.set(f"Last: {event.keysym}  (logged)")

def clear_log():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        status.set("Log cleared.")
    else:
        status.set("No log to clear.")

def show_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        # Show small window with log content
        win = tk.Toplevel(root)
        win.title("Log contents")
        text = tk.Text(win, wrap="none", width=80, height=20)
        text.insert("1.0", content)
        text.config(state="disabled")
        text.pack(fill="both", expand=True)
    else:
        status.set("Log file not found.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("In-app Key Logger (educational)")

    instructions = tk.Label(root, text=(
        "This app logs key presses *only while this window is focused*.\n"
        "Use the input area below or press keys while the window is active.\n"
        "Do NOT use this to capture others' keystrokes without consent."
    ))
    instructions.pack(padx=10, pady=10)

    # A text widget so user can type (or press keys anywhere in the window)
    txt = tk.Text(root, height=6, width=60)
    txt.pack(padx=10, pady=(0,10))
    txt.focus_set()

    # Status bar
    status = tk.StringVar(value="Ready.")
    status_label = tk.Label(root, textvariable=status, anchor="w")
    status_label.pack(fill="x", padx=10, pady=(0,10))

    # Buttons
    btn_frame = tk.Frame(root)
    tk.Button(btn_frame, text="Show Log", command=show_log).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Clear Log", command=clear_log).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Exit", command=root.destroy).pack(side="left", padx=5)
    btn_frame.pack(pady=(0,10))

    # Bind key press events to the root window (fires only when window has focus)
    root.bind_all("<KeyPress>", log_key)

    root.mainloop()
