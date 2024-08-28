import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
from domain.database import session
from domain.containers import Container
from domain.sensor import Sensor

CACHE_SIZE = 5

def update_container_details(frame, container):
    for widget in frame.winfo_children():
        widget.destroy()

    sensor_data_cache = {
        "moisture": [],
        "light": [],
        "soil": []
    }


    info_frame = tk.Frame(frame)
    info_frame.pack(fill=tk.BOTH, padx=10, pady=10)

    if container.plant and container.plant.image_path:
        image = load_image(container.plant.image_path)
        if image:
            image_label = tk.Label(info_frame, image=image)
            image_label.image = image 
            image_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky='n')
        else:
            tk.Label(info_frame, text="Image not available").grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky='n')

    details_frame = tk.Frame(info_frame)
    details_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

    tk.Label(details_frame, text=f"Material: {container.container_material}", font=("Arial", 14)).pack(anchor='w', pady=5)
    tk.Label(details_frame, text=f"Location: {container.container_location}", wraplength=400).pack(anchor='w', pady=5)

    sensors = session.query(Sensor).filter_by(container_id=container.container_id).all()
    for sensor in sensors:
        if sensor.sensor_type == "moisture":
            sensor_data_cache["moisture"].append(sensor.moisture)
        elif sensor.sensor_type == "light":
            sensor_data_cache["light"].append(sensor.light)
        elif sensor.sensor_type == "soil":
            sensor_data_cache["soil"].append(sensor.soil)

    if (not container.is_empty):
        sensor_data = display_sensor_info(details_frame, sensors, sensor_data_cache)

    graph_frame = tk.Frame(frame)
    graph_frame.pack(fill=tk.BOTH, padx=10, pady=20, expand=True)

    graph_types = ['line', 'pie', 'histogram']
    current_graph_index = [0]

    def display_graph():
        """Displays the current graph based on the graph index."""
        for widget in graph_frame.winfo_children():
            widget.destroy()

        graph_type = graph_types[current_graph_index[0]]

        if graph_type == 'line':
            create_line_chart(graph_frame, sensor_data_cache)
        elif graph_type == 'pie':
            create_pie_chart(graph_frame, sensor_data_cache)
        elif graph_type == 'histogram':
            create_histogram(graph_frame, sensor_data_cache)

    def cycle_graph():
        """Cycles to the next graph type."""
        current_graph_index[0] = (current_graph_index[0] + 1) % len(graph_types)
        display_graph()

    display_graph_button = tk.Button(frame, text="Next Graph", command=cycle_graph)
    display_graph_button.pack(pady=10)

    display_graph()

    nav_frame = tk.Frame(frame)
    nav_frame.pack(pady=20)

    def show_previous_container():
        if (session.query(Container).count() == 1):
            return
        previous_container = session.query(Container).filter(Container.container_id < container.container_id).order_by(Container.container_id.desc()).first()
        if previous_container is None:
            previous_container = session.query(Container).order_by(Container.container_id.desc()).first()
        update_container_details(frame, previous_container)

    def show_next_container():
        if (session.query(Container).count() == 1):
            return
        next_container = session.query(Container).filter(Container.container_id > container.container_id).order_by(Container.container_id.asc()).first()
        if next_container is None:
            next_container = session.query(Container).order_by(Container.container_id.asc()).first()
        update_container_details(frame, next_container)

    previous_button = tk.Button(nav_frame, text="Previous", command=show_previous_container)
    previous_button.pack(side=tk.LEFT, padx=10)

    next_button = tk.Button(nav_frame, text="Next", command=show_next_container)
    next_button.pack(side=tk.RIGHT, padx=10)

    if (not container.is_empty):
        sync_button = tk.Button(frame, text="Sync Data", 
                            command=lambda: sync_sensor_data(container, sensor_data_cache, details_frame, graph_frame, 
                                                             display_graph))
        sync_button.pack(pady=10)   



def create_line_chart(parent, sensor_data):
    fig, ax = plt.subplots()
    if sensor_data['moisture']:
        ax.plot(sensor_data['moisture'], label='Moisture')
    if sensor_data['light']:
        ax.plot(sensor_data['light'], label='Light')
    if sensor_data['soil']:
        ax.plot(sensor_data['soil'], label='Soil')
    ax.set_title("Line Chart")
    ax.legend()

    # Embed the plot in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def create_pie_chart(parent, sensor_data):
    fig, ax = plt.subplots()
    labels = []
    sizes = []
    if sensor_data['moisture']:
        labels.append('Moisture')
        sizes.append(sum(sensor_data['moisture']))
    if sensor_data['light']:
        labels.append('Light')
        sizes.append(sum(sensor_data['light']))
    if sensor_data['soil']:
        labels.append('Soil')
        sizes.append(sum(sensor_data['soil']))

    if sizes: 
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  
        ax.set_title("Pie Chart")

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def create_histogram(parent, sensor_data):
    """Creates a histogram and embeds it in the provided frame."""
    fig, ax = plt.subplots()
    data = []
    if sensor_data['moisture']:
        data.extend(sensor_data['moisture'])
    if sensor_data['light']:
        data.extend(sensor_data['light'])
    if sensor_data['soil']:
        data.extend(sensor_data['soil'])

    if data: 
        ax.hist(data, bins=10, alpha=0.7, color='blue')
        ax.set_title("Histogram")

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def load_image(image_path):
    """Loads an image from the given path and returns a PhotoImage object."""
    try:
        img = Image.open(image_path)
        img = img.resize((100, 100), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None

def initialize_container_details(frame):
    container = session.query(Container).first() 
    if container:
        update_container_details(frame, container)
    else:
        tk.Label(frame, text="No containers available.", font=("Arial", 14)).pack(pady=20)

def sync_sensor_data(container, sensor_data_cache, details_frame, graph_frame, display_graph):
    sensors = session.query(Sensor).filter_by(container_id=container.container_id).all()
    for sensor in sensors:
        if sensor.sensor_type == "light":
            sensor_data_cache["light"].append(sensor.light)
            sensor.light = random.uniform(0, 100)
            # Keep only the last CACHE_SIZE readings
            if len(sensor_data_cache["light"]) > CACHE_SIZE:
                sensor_data_cache["light"] = sensor_data_cache["light"][-CACHE_SIZE:]
        elif sensor.sensor_type == "moisture":
            sensor_data_cache["moisture"].append(sensor.moisture)
            sensor.moisture = random.uniform(0, 100)
            if len(sensor_data_cache["moisture"]) > CACHE_SIZE:
                sensor_data_cache["moisture"] = sensor_data_cache["moisture"][-CACHE_SIZE:]
        elif sensor.sensor_type == "soil":
            sensor_data_cache["soil"].append(sensor.soil)
            sensor.soil = random.uniform(5, 7.5)
            if len(sensor_data_cache["soil"]) > CACHE_SIZE:
                sensor_data_cache["soil"] = sensor_data_cache["soil"][-CACHE_SIZE:]

        session.commit()
    sensor_data = display_sensor_info(details_frame, sensors, sensor_data_cache)
    display_graph() 

def display_sensor_info(details_frame, sensors, sensor_data_cache):
    for widget in details_frame.winfo_children():
        widget.destroy()

    if sensors:
        tk.Label(details_frame, text="Sensors:", font=("Arial", 12)).pack(anchor='w', pady=10)
        for sensor in sensors:
            sensor_info = f"Sensor: {sensor.sensor_type} ("
            if sensor.moisture is not None:
                sensor_info += f"Moisture: {sensor.moisture:.2f}"
            if sensor.light is not None:
                if "Moisture" in sensor_info:
                    sensor_info += ", "
                sensor_info += f"Light: {sensor.light:.2f}"
            if sensor.soil is not None:
                if "Moisture" in sensor_info or "Light" in sensor_info:
                    sensor_info += ", "
                sensor_info += f"Soil: {sensor.soil:.2f}"
            sensor_info += ")"
            tk.Label(details_frame, text=sensor_info).pack(anchor='w', pady=5)
