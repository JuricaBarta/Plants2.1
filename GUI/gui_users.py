import tkinter as tk
from tkinter import messagebox
from domain.database import session
from domain.user import User, create_user, update_user, delete_user

def initialize_user_window(parent_frame):
    user_window = tk.Toplevel(parent_frame)
    user_window.title("User Management")
    user_window.geometry("600x400")

    details_frame = tk.Frame(user_window)
    details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    listbox_frame = tk.Frame(user_window)
    listbox_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(listbox_frame, text="Users").pack()

    user_listbox = tk.Listbox(listbox_frame)
    user_listbox.pack(fill=tk.BOTH, expand=True)

    def refresh_user_list():
        user_listbox.delete(0, tk.END)
        users = session.query(User).all()
        for u in users:
            user_listbox.insert(tk.END, f"{u.username}")

    refresh_user_list()

    tk.Label(details_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
    name_entry = tk.Entry(details_frame)
    name_entry.grid(row=0, column=1, sticky=tk.EW)

    tk.Label(details_frame, text="Surname:").grid(row=1, column=0, sticky=tk.W)
    surname_entry = tk.Entry(details_frame)
    surname_entry.grid(row=1, column=1, sticky=tk.EW)

    tk.Label(details_frame, text="Username:").grid(row=2, column=0, sticky=tk.W)
    username_entry = tk.Entry(details_frame)
    username_entry.grid(row=2, column=1, sticky=tk.EW)

    tk.Label(details_frame, text="Password:").grid(row=3, column=0, sticky=tk.W)
    password_entry = tk.Entry(details_frame, show="*")
    password_entry.grid(row=3, column=1, sticky=tk.EW)

    def update_entries(selected_user):
        name_entry.delete(0, tk.END)
        name_entry.insert(0, selected_user.name)

        surname_entry.delete(0, tk.END)
        surname_entry.insert(0, selected_user.surname)

        username_entry.delete(0, tk.END)
        username_entry.insert(0, selected_user.username)

        password_entry.delete(0, tk.END)
        password_entry.insert(0, selected_user.password)

    def clear_entries():
        name_entry.delete(0, tk.END)
        surname_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        user_listbox.selection_clear(0, tk.END)

    def on_user_select(event):
        selected_index = user_listbox.curselection()
        if selected_index:
            selected_user = session.query(User).all()[selected_index[0]]
            update_entries(selected_user)

    user_listbox.bind('<<ListboxSelect>>', on_user_select)

    # Deselect button
    deselect_button = tk.Button(details_frame, text="Deselect", command=clear_entries)
    deselect_button.grid(row=4, column=0, columnspan=2, pady=10)

    def save_user():
        name = name_entry.get()
        surname = surname_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        selected_index = user_listbox.curselection()

        if selected_index:
            selected_user = session.query(User).all()[selected_index[0]]
            update_user(
                user_id=selected_user.user_id, 
                name=name,
                surname=surname,
                username=username,
                password=password
            )
        else:
            create_user(
                session=session,
                name=name, 
                surname=surname, 
                username=username, 
                password=password
            )

        refresh_user_list()
        clear_entries()

    save_button = tk.Button(details_frame, text="Save", command=save_user)
    save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def delete_user_action():
        selected_index = user_listbox.curselection()
        if selected_index:
            selected_user = session.query(User).all()[selected_index[0]]
            if (selected_user.user_id == 1):
                return
            delete_user(session, selected_user.user_id)
            refresh_user_list()
            clear_entries()

    delete_button = tk.Button(details_frame, text="Delete", command=delete_user_action)
    delete_button.grid(row=6, column=0, columnspan=2, pady=10)
