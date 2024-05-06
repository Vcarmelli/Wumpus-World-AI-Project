import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import webbrowser

def open_repo_link():
    webbrowser.open("https://your_git_repository_link_here")

def quit_game():
    quit()

def custom_message_box():
    custom_dialog = tk.Toplevel(bg="white")
    custom_dialog.title("Confirmation")
    message_label = tk.Label(custom_dialog, text="Click here to explore the Git repository.", fg="blue", cursor="hand2", bg="white")
    message_label.pack(padx=20, pady=10)
    message_label.bind("<Button-1>", lambda event: open_repo_link())
    
    # Create a custom style for rounded corners and depth
    custom_style = ttk.Style()
    custom_style.configure("Custom.TButton", borderwidth=0, relief="solid", borderradius=5, background="white", highlightthickness=5)


    no_button = ttk.Button(custom_dialog, text="No", style="Custom.TButton", command=custom_dialog.destroy)
    no_button.pack(side="right", padx=(5, 25), pady=15)
    yes_button = ttk.Button(custom_dialog, text="Yes", style="Custom.TButton", command=quit_game)
    yes_button.pack(side="right", padx=(25, 5), pady=15)

root = tk.Tk()
root.geometry("300x200")

quit_button = tk.Button(root, text="Quit Game", command=custom_message_box)
quit_button.pack(pady=20)

root.mainloop()
