import tkinter as tk
from tkinter import ttk, messagebox
from domain.database import session
from domain.user import *
from .gui import open_main_app

def run_login_screen():
    login_window = tk.Tk()
    login_window.title("Prijava")
    login_window.geometry("600x400")
    login_window.resizable(False, False)  

    frame = tk.Frame(login_window)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    tk.Label(frame, text="Username", font=("Arial", "12")).grid(row=0, column=0, padx=10, pady=10)
    entry_username = tk.Entry(frame)
    entry_username.grid(row=1, column=0, padx=10, pady=10)

    tk.Label(frame, text="Password", font=("Arial", "12")).grid(row=2, column=0, padx=10, pady=10)
    entry_password = tk.Entry(frame, show="*")
    entry_password.grid(row=3, column=0, padx=10, pady=10)

    password_show = tk.IntVar(value=0)
    def hide_password():
        if password_show.get() == 1:
            entry_password.config(show="")
        else:
            entry_password.config(show="*")

    tk.Checkbutton(frame, text="Show password", font="Arial", variable=password_show, command=hide_password).grid(row=4, column=0, padx=10, pady=10)

    tk.Button(frame, text="Login", command=lambda: handle_login(entry_username, entry_password, login_window)).grid(row=5, column=0, padx=10, pady=20)

    login_window.mainloop()

def validate_login(username, password):
    user = get_user_by_username(session, username)
    if user and user.password == password:
        return True
    return False

def handle_login(entry_username, entry_password, login_window):
    username = entry_username.get()
    password = entry_password.get()
    
    if validate_login(username, password):
        login_window.destroy()
        open_main_app()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")
