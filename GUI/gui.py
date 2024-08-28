import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import close_all_sessions
from domain.database import session
from domain.user import *
from domain.plants import Plant
from domain.containers import Container
from domain.sensor import Sensor
from .gui_containers import *
from .gui_container_details import *
from .gui_plants import *
from .gui_login import *
from .gui_users import *

def open_main_app():
    global main_app 
    main_app = tk.Tk()
    main_app.title("Algebra")
    main_app.geometry("1200x1000")

    notebook = ttk.Notebook(main_app)
    notebook.pack(pady=10, expand=True)

    container_overview_frame = ttk.Frame(notebook)
    notebook.add(container_overview_frame, text='Container Overview')

    container_details_frame = ttk.Frame(notebook)
    notebook.add(container_details_frame, text='Container Details')

    plant_overview_frame = ttk.Frame(notebook)
    notebook.add(plant_overview_frame, text='Plant Overview')

    plant_details_frame = ttk.Frame(notebook)
    notebook.add(plant_details_frame, text='Plant Details')

    user_frame = ttk.Frame(notebook)
    notebook.add(user_frame, text='User management')

    initialize_container_overview(container_overview_frame, notebook)
    
    first_container = session.query(Container).first()
    if first_container:
        update_container_details(container_details_frame, first_container)
    else:
        tk.Label(container_details_frame, text="No containers available.", font=("Arial", 14)).pack(pady=20)

    initialize_plant_overview(plant_overview_frame, notebook)
    initialize_plant_details(plant_details_frame)
    
    manage_users_button = tk.Button(user_frame, text="Manage Users", command=lambda: initialize_user_window(user_frame))
    manage_users_button.pack(pady=20)

    main_app.protocol("WM_DELETE_WINDOW", on_closing)

    main_app.mainloop()

def on_closing():
    close_all_sessions() 
    engine.dispose()
    main_app.quit()
    main_app.destroy() 
