import tkinter as tk
from tkinter import ttk

# List of abusive/racist words
bad_words = ["bsdk", "raand", "randi", "madharchod", "randwa", "chutiya", "jhaat", "lund", "chut", "choochi", "chod", "behenchod", "gaand", "fuck", "dumb", "nigga", "nigger", "maa ki chut", "behen ki chut", "behen ka loda", "behn ka loda", "behn ke lode", "randi ke dalal", "chodal", "chinnar", "fuckass", "sex", "rape", "black", "rand", "gand", "choochi", "bhosdi", "bhosda", "bhosdike", "bhosdika", "dalal", "nigger", "black", "land", "bhosad", "chewt", "chodna", "muth", "spaerm", "chutad", "muh me", "lauda", "boobs", "vagina", "penis", "ling", "chinri"]

# Themes
dark_theme = {
    "bg": "#121212",
    "text_bg": "#1e1e1e",
    "fg": "white",
    "button_bg": "#8a2be2",
    "button_fg": "white",
    "result_fg_clean": "lightgreen",
    "result_fg_bad": "red",
    "checking_fg": "yellow",
}
light_theme = {
    "bg": "white",
    "text_bg": "white",
    "fg": "black",
    "button_bg": "#7a1dd1",
    "button_fg": "white",
    "result_fg_clean": "green",
    "result_fg_bad": "red",
    "checking_fg": "orange",
}

current_theme = dark_theme

# Function to apply theme colors
def apply_theme(theme):
    root.configure(bg=theme["bg"])
    title.config(bg=theme["bg"], fg=theme["fg"])
    text_area.config(bg=theme["text_bg"], fg=theme["fg"], insertbackground=theme["fg"])
    check_button.config(bg=theme["button_bg"], fg=theme["button_fg"],
                        activebackground=theme["button_bg"])
    toggle_button.config(bg=theme["button_bg"], fg=theme["button_fg"],
                         activebackground=theme["button_bg"])
    result_label.config(bg=theme["bg"], fg=theme["fg"])
    disclaimer.config(bg=theme["bg"], fg="gray")
    meter_style.configure("blue.Horizontal.TProgressbar", troughcolor=theme["bg"])

# Function to check the paragraph
def check_text():
    text = text_area.get("1.0", tk.END).lower()
    found = [word for word in bad_words if word in text]
    count = len(found)
    max_count = 10  # max for meter cap
    meter_value = min(count, max_count) / max_count * 100
    profanity_meter['value'] = meter_value
    
    if count > 0:
        result_label.config(
            text=f"Inappropriate words found: {', '.join(found)}",
            fg=current_theme["result_fg_bad"])
    else:
        result_label.config(
            text="No abusive or racist language found.",
            fg=current_theme["result_fg_clean"])
    stop_checking_animation()

# Animation for checking message
anim_running = False
def blink_checking():
    if not anim_running:
        return
    current_color = result_label.cget("fg")
    next_color = current_theme["checking_fg"] if current_color != current_theme["checking_fg"] else current_theme["bg"]
    result_label.config(fg=next_color)
    root.after(500, blink_checking)

def show_checking_message():
    global anim_running
    anim_running = True
    result_label.config(text="Checking paragraph...", fg=current_theme["checking_fg"])
    blink_checking()
    root.after(1500, check_text)

def stop_checking_animation():
    global anim_running
    anim_running = False
    result_label.config(fg=current_theme["fg"])

# Enter key handler
def enter_pressed(event):
    show_checking_message()
    return "break"

# Toggle theme
def toggle_theme():
    global current_theme
    current_theme = light_theme if current_theme == dark_theme else dark_theme
    apply_theme(current_theme)

# Set up the main window
root = tk.Tk()
root.title("Abuse & Racism Checker")
root.geometry("600x500")
root.configure(bg=current_theme["bg"])

# Title label
title = tk.Label(root, text="Type your paragraph below",
                 font=("Arial", 16), bg=current_theme["bg"], fg=current_theme["fg"])
title.pack(pady=10)

# Text area
text_area = tk.Text(root, height=10, wrap="word", font=("Arial", 12),
                    bg=current_theme["text_bg"], fg=current_theme["fg"], insertbackground=current_theme["fg"], bd=2, relief="solid")
text_area.pack(padx=20, pady=10, fill="both", expand=True)
text_area.bind("<Return>", enter_pressed)

# Buttons frame
btn_frame = tk.Frame(root, bg=current_theme["bg"])
btn_frame.pack(pady=5)

# Check button
check_button = tk.Button(btn_frame, text="Check for Bad Words", command=check_text,
                         font=("Arial", 12), bg=current_theme["button_bg"], fg=current_theme["button_fg"], activebackground=current_theme["button_bg"], relief="raised", bd=2)
check_button.pack(side="left", padx=10)

# Toggle theme button
toggle_button = tk.Button(btn_frame, text="Toggle Dark/Light Mode", command=toggle_theme,
                          font=("Arial", 12), bg=current_theme["button_bg"], fg=current_theme["button_fg"], activebackground=current_theme["button_bg"], relief="raised", bd=2)
toggle_button.pack(side="left", padx=10)

# Profanity Meter label
meter_label = tk.Label(root, text="Profanity Level:", font=("Arial", 12), bg=current_theme["bg"], fg=current_theme["fg"])
meter_label.pack(pady=(10, 0))

# Profanity Meter progress bar
meter_style = ttk.Style()
meter_style.theme_use('default')
meter_style.configure("blue.Horizontal.TProgressbar", troughcolor=current_theme["bg"], bordercolor=current_theme["bg"], background="#8a2be2", lightcolor="#a64dff", darkcolor="#6a1db7")

profanity_meter = ttk.Progressbar(root, style="blue.Horizontal.TProgressbar", orient="horizontal", length=400, mode="determinate", maximum=100)
profanity_meter.pack(pady=(0, 10))

# Result label
result_label = tk.Label(root, text="", font=("Arial", 12),
                        bg=current_theme["bg"], fg=current_theme["fg"], wraplength=500)
result_label.pack(pady=10)

# Disclaimer label
disclaimer = tk.Label(root,
                      text="Note: This program may not detect all forms of abusive or racist language.",
                      font=("Arial", 10), bg=current_theme["bg"], fg="gray")
disclaimer.pack(side="bottom", pady=10)

apply_theme(current_theme)

root.mainloop()
