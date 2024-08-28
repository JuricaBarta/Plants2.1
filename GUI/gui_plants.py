import tkinter as tk
from PIL import Image, ImageTk
from domain.database import *
from domain.plants import *
from domain.sensor import *
from .gui_plant_actions import open_plant_details_window

def initialize_plant_overview(frame, notebook):
    for widget in frame.winfo_children():
        widget.destroy()

    label = tk.LabelFrame(frame, text="Plants Overview")
    label.grid(padx=10, pady=10, sticky='nsew')

    canvas = tk.Canvas(label, highlightthickness=0, width=800, height=900)
    canvas.grid(row=0, column=0, sticky='nsew')

    scrollbar_y = tk.Scrollbar(label, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar_y.grid(row=0, column=1, sticky='ns')
    canvas.config(yscrollcommand=scrollbar_y.set)

    scrollbar_x = tk.Scrollbar(label, orient=tk.HORIZONTAL, command=canvas.xview)
    scrollbar_x.grid(row=1, column=0, sticky='ew')
    canvas.config(xscrollcommand=scrollbar_x.set)

    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor='nw')

    def create_plant_frame(plant, row, column):
        plant_frame = tk.Frame(inner_frame, borderwidth=1, relief=tk.RAISED, width=350, height=150)
        plant_frame.grid(row=row, column=column, padx=5, pady=5, sticky='nsew')

        image = load_image(plant.image_path)
        if image:
            image_label = tk.Label(plant_frame, image=image)
            image_label.image = image
            image_label.pack(side=tk.LEFT, padx=5, pady=5)
        else:
            image_label = tk.Label(plant_frame, text="Image not available", relief=tk.RAISED, width=20, height=10)
            image_label.pack(side=tk.LEFT, padx=5, pady=5)

        text_frame = tk.Frame(plant_frame)
        text_frame.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.BOTH, expand=True)

        name_label = tk.Label(text_frame, text=plant.plant_name, font=("Arial", 12), anchor='w')
        name_label.pack(fill=tk.X, padx=5, pady=5)

        description_label = tk.Label(text_frame, text=plant.plant_description, anchor='w', wraplength=200)
        description_label.pack(fill=tk.BOTH, padx=5, pady=5)

        plant_frame.bind("<Button-1>", lambda e: open_plant_details_tab(notebook, plant))

    def open_plant_details_tab(notebook, plant):
        for tab in notebook.tabs():
            if notebook.tab(tab, "text") == "Plant Details":
                notebook.select(tab) 
                plant_details_frame = notebook.nametowidget(tab)
                update_plant_details(plant_details_frame, plant)
                break

    def create_labels():
        plants = get_all_plants()

        num_cols = 2 
        num_rows = (len(plants) + num_cols) // num_cols

        for i, plant in enumerate(plants):
            row = i // num_cols
            column = i % num_cols
            create_plant_frame(plant, row, column)

        add_plant_row = len(plants) // num_cols
        add_plant_col = len(plants) % num_cols

        add_plant_frame = tk.Frame(inner_frame, borderwidth=1, relief=tk.RAISED, width=350, height=150)
        add_plant_frame.grid(row=add_plant_row, column=add_plant_col, padx=5, pady=5, sticky='nsew')

        add_plant_button = tk.Button(add_plant_frame, text="Add Plant", command=lambda: open_plant_details_window(None, frame, notebook), relief=tk.RAISED)
        add_plant_button.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        for i in range(add_plant_row + 1):
            inner_frame.grid_rowconfigure(i, weight=1)
        for i in range(num_cols):
            inner_frame.grid_columnconfigure(i, weight=1)

    create_labels()

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    inner_frame.bind('<Configure>', on_frame_configure)

    def on_mousewheel(event):
        """Handle mouse wheel scrolling."""
        if event.delta > 0:
            canvas.yview_scroll(-1, 'units')
        else:
            canvas.yview_scroll(1, 'units')

    canvas.bind_all('<MouseWheel>', on_mousewheel)

    canvas.bind_all('<Button-4>', lambda event: canvas.yview_scroll(-1, 'units'))
    canvas.bind_all('<Button-5>', lambda event: canvas.yview_scroll(1, 'units'))


def initialize_plant_details(frame):
    plant = session.query(Plant).first()  
    if plant:
        update_plant_details(frame, plant)
    else:
        tk.Label(frame, text="No plants available.", font=("Arial", 14)).pack(pady=20)

def update_plant_details(frame, plant):
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text=f"Name: {plant.plant_name}", font=("Arial", 14)).pack(pady=10)
    tk.Label(frame, text=f"Description: {plant.plant_description}", wraplength=400).pack(pady=10)
    tk.Label(frame, text=f"Moisture Info: {plant.moisture_info}").pack(pady=10)
    tk.Label(frame, text=f"Light/Temperature Info: {plant.light_temp_info}").pack(pady=10)
    tk.Label(frame, text=f"Substrates: {plant.substrates}").pack(pady=10)

    if plant.image_path:
        image = load_image(plant.image_path)
        if image:
            tk.Label(frame, image=image).pack(pady=10)
            frame.image = image  
        else:
            tk.Label(frame, text="Image not available").pack(pady=10)

    nav_frame = tk.Frame(frame)
    nav_frame.pack(pady=20)

    def show_previous_plant():
        previous_plant = session.query(Plant).filter(Plant.plant_id < plant.plant_id).order_by(Plant.plant_id.desc()).first()
        if previous_plant is None:
            previous_plant = session.query(Plant).order_by(Plant.plant_id.desc()).first()
        update_plant_details(frame, previous_plant)

    def show_next_plant():
        next_plant = session.query(Plant).filter(Plant.plant_id > plant.plant_id).order_by(Plant.plant_id.asc()).first()
        if next_plant is None:
            next_plant = session.query(Plant).order_by(Plant.plant_id.asc()).first()
        update_plant_details(frame, next_plant)

    previous_button = tk.Button(nav_frame, text="Previous", command=show_previous_plant)
    previous_button.pack(side=tk.LEFT, padx=10)

    next_button = tk.Button(nav_frame, text="Next", command=show_next_plant)
    next_button.pack(side=tk.RIGHT, padx=10)

def load_image(image_path):
    try:
        img = Image.open(image_path)
        img = img.resize((100, 100), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None
