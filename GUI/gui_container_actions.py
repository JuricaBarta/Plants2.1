import tkinter as tk
import random
from domain.database import session
from domain.containers import Container, create_container, update_container, delete_container
from domain.plants import get_all_plants, Plant
from domain.sensor import Sensor, create_sensor

def open_container_details_window(parent_frame, update_overview_func):
    """Opens a window to view, create, edit, or delete containers."""
    container_window = tk.Toplevel(parent_frame)
    container_window.title("Container Details")
    container_window.geometry("600x400")

    details_frame = tk.Frame(container_window)
    details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    listbox_frame = tk.Frame(container_window)
    listbox_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(listbox_frame, text="Containers").pack()

    container_listbox = tk.Listbox(listbox_frame)
    container_listbox.pack(fill=tk.BOTH, expand=True)

    containers = session.query(Container).all()
    for c in containers:
        container_listbox.insert(tk.END, f"Container {c.container_id}")

    tk.Label(details_frame, text="Container Material:").grid(row=0, column=0, sticky=tk.W)
    material_entry = tk.Entry(details_frame)
    material_entry.grid(row=0, column=1, sticky=tk.EW)

    tk.Label(details_frame, text="Location:").grid(row=1, column=0, sticky=tk.W)
    location_entry = tk.Entry(details_frame)
    location_entry.grid(row=1, column=1, sticky=tk.EW)

    tk.Label(details_frame, text="Plant:").grid(row=2, column=0, sticky=tk.W)
    plant_var = tk.StringVar(details_frame)
    plant_menu = tk.OptionMenu(details_frame, plant_var, *["None"] + [plant.plant_name for plant in get_all_plants()])
    plant_menu.grid(row=2, column=1, sticky=tk.EW)

    def update_entries(selected_container):
        material_entry.delete(0, tk.END)
        material_entry.insert(0, selected_container.container_material)

        location_entry.delete(0, tk.END)
        location_entry.insert(0, selected_container.container_location)

        if selected_container.plant:
            plant_var.set(selected_container.plant.plant_name)
        else:
            plant_var.set("None")

    def clear_entries():
        material_entry.delete(0, tk.END)
        location_entry.delete(0, tk.END)
        plant_var.set("None")
        container_listbox.selection_clear(0, tk.END)

    def on_container_select(event):
        selected_index = container_listbox.curselection()
        if selected_index:
            selected_container = containers[selected_index[0]]
            update_entries(selected_container)

    container_listbox.bind('<<ListboxSelect>>', on_container_select)

    deselect_button = tk.Button(details_frame, text="Deselect", command=clear_entries)
    deselect_button.grid(row=3, column=0, columnspan=2, pady=10)

    def save_container():
        material = material_entry.get()
        location = location_entry.get()
        selected_plant_name = plant_var.get()

        selected_plant = None
        if selected_plant_name != "None":
            selected_plant = session.query(Plant).filter_by(plant_name=selected_plant_name).first()

        selected_index = container_listbox.curselection()

        if selected_index:
            selected_container = containers[selected_index[0]]
            update_container(
                container_id=selected_container.container_id, 
                container_material=material, 
                container_location=location, 
                plant_id=selected_plant.plant_id if selected_plant else None
            )
        else:
            new_container = create_container(
                container_material=material, 
                container_location=location, 
                plant_id=selected_plant.plant_id if selected_plant else None
            )

            if new_container and new_container.container_id:
                create_sensor(
                    container_id=new_container.container_id,
                    sensor_type="light",
                    light=random.uniform(0, 100)
                )

                create_sensor(
                    container_id=new_container.container_id,
                    sensor_type="moisture",
                    moisture=random.uniform(0, 100)
                )

                create_sensor(
                    container_id=new_container.container_id,
                    sensor_type="soil",
                    soil=random.uniform(5, 7.5)
                )
            else:
                print("Error: Container ID is not available.")

        container_window.destroy()

        update_overview_func(parent_frame)

    save_button = tk.Button(details_frame, text="Save", command=save_container)
    save_button.grid(row=4, column=0, columnspan=2, pady=10)

    def delete_container_action():
        """Deletes the selected container."""
        selected_index = container_listbox.curselection()
        if selected_index:
            selected_container = containers[selected_index[0]]
            delete_container(selected_container.container_id)
            container_window.destroy()
            update_overview_func(parent_frame)

    delete_button = tk.Button(details_frame, text="Delete", command=delete_container_action)
    delete_button.grid(row=5, column=0, columnspan=2, pady=10)