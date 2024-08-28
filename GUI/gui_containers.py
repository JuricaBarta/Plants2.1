import tkinter as tk
from PIL import Image, ImageTk
from domain.database import session
from domain.containers import Container
from .gui_container_actions import open_container_details_window
from .gui_container_details import update_container_details

def initialize_container_overview(frame, notebook):
    for widget in frame.winfo_children():
        widget.destroy()

    label = tk.LabelFrame(frame, text="Containers Overview")
    label.grid(padx=10, pady=10, sticky='nsew')

    filter_frame = tk.Frame(label)
    filter_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

    filter_var = tk.StringVar(value="All")
    filter_label = tk.Label(filter_frame, text="Filter by Empty Status:")
    filter_label.pack(side=tk.LEFT, padx=5)
    filter_menu = tk.OptionMenu(filter_frame, filter_var, "All", "Empty", "Non-Empty", command=lambda _: create_labels())
    filter_menu.pack(side=tk.LEFT, padx=5)

    canvas = tk.Canvas(label, highlightthickness=0, width=800, height=900)
    canvas.grid(row=1, column=0, sticky='nsew')

    scrollbar_y = tk.Scrollbar(label, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar_y.grid(row=1, column=1, sticky='ns')
    canvas.config(yscrollcommand=scrollbar_y.set)

    scrollbar_x = tk.Scrollbar(label, orient=tk.HORIZONTAL, command=canvas.xview)
    scrollbar_x.grid(row=2, column=0, sticky='ew')
    canvas.config(xscrollcommand=scrollbar_x.set)

    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor='nw')

    def create_container_frame(container, row, column):
        container_frame = tk.Frame(inner_frame, borderwidth=1, relief=tk.RAISED, width=350, height=150)
        container_frame.grid(row=row, column=column, padx=5, pady=5, sticky='nsew')

        text_frame = tk.Frame(container_frame)
        text_frame.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.BOTH, expand=True)

        tk.Label(text_frame, text=f"Material: {container.container_material}", font=("Arial", 12), anchor='w').pack(fill=tk.X, padx=5, pady=5)
        tk.Label(text_frame, text=f"Location: {container.container_location}", anchor='w').pack(fill=tk.X, padx=5, pady=5)
        tk.Label(text_frame, text=f"Empty: {'Yes' if container.is_empty else 'No'}", anchor='w').pack(fill=tk.X, padx=5, pady=5)

        if not container.is_empty and container.plant:
            plant = container.plant
            plant_name_label = tk.Label(text_frame, text=f"Plant: {plant.plant_name}", anchor='w')
            plant_name_label.pack(fill=tk.X, padx=5, pady=5)

            if plant.image_path:
                image = load_image(plant.image_path)
                if image:
                    image_label = tk.Label(container_frame, image=image)
                    image_label.image = image
                    image_label.pack(side=tk.LEFT, padx=5, pady=5)

        container_frame.bind("<Button-1>", lambda e: open_container_details_tab(notebook, container))


    def open_container_details_tab(notebook, container):
        for tab in notebook.tabs():
            if notebook.tab(tab, "text") == "Container Details":
                notebook.select(tab)
                container_details_frame = notebook.nametowidget(tab)
                update_container_details(container_details_frame, container)
                break

    def create_labels():
        filter_option = filter_var.get()

        if filter_option == "Empty":
            containers = session.query(Container).filter_by(is_empty=True).all()
        elif filter_option == "Non-Empty":
            containers = session.query(Container).filter_by(is_empty=False).all()
        else: 
            containers = session.query(Container).all()

        for widget in inner_frame.winfo_children():
            widget.destroy()

        num_cols = 2  
        num_rows = (len(containers) + num_cols) // num_cols 
        for i, container in enumerate(containers):
            row = i // num_cols
            column = i % num_cols
            create_container_frame(container, row, column)

        add_container_row = len(containers) // num_cols
        add_container_col = len(containers) % num_cols

        add_container_frame = tk.Frame(inner_frame, borderwidth=1, relief=tk.RAISED, width=350, height=150)
        add_container_frame.grid(row=add_container_row, column=add_container_col, padx=5, pady=5, sticky='nsew')

        add_container_button = tk.Button(
            add_container_frame,
            text="Add Container",
            command=lambda: open_container_details_window(frame, lambda f, n=notebook: initialize_container_overview(f, n)),
            relief=tk.RAISED
        )
        add_container_button.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        for i in range(add_container_row + 1):
            inner_frame.grid_rowconfigure(i, weight=1)
        for i in range(num_cols):
            inner_frame.grid_columnconfigure(i, weight=1)

    create_labels()

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    inner_frame.bind('<Configure>', on_frame_configure)

    def on_mousewheel(event):
        if event.delta > 0:
            canvas.yview_scroll(-1, 'units')
        else:
            canvas.yview_scroll(1, 'units')

    canvas.bind_all('<MouseWheel>', on_mousewheel)

    canvas.bind_all('<Button-4>', lambda event: canvas.yview_scroll(-1, 'units'))
    canvas.bind_all('<Button-5>', lambda event: canvas.yview_scroll(1, 'units'))

def load_image(image_path):
    try:
        img = Image.open(image_path)
        img = img.resize((100, 100), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None