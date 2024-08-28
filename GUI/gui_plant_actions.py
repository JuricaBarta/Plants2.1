import tkinter as tk
from domain.plants import *

def open_plant_details_window(plant, parent_window, notebook):
    plant_window = tk.Toplevel(parent_window)
    plant_window.title("Plant Details")
    plant_window.geometry("600x400")

    # Frame for plant details
    details_frame = tk.Frame(plant_window)
    details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Frame for plant list
    listbox_frame = tk.Frame(plant_window)
    listbox_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(listbox_frame, text="Plants").pack()

    plant_listbox = tk.Listbox(listbox_frame)
    plant_listbox.pack(fill=tk.BOTH, expand=True)

    plants = get_all_plants()
    for p in plants:
        plant_listbox.insert(tk.END, p.plant_name)

    tk.Label(details_frame, text="Plant Name:").grid(row=0, column=0, sticky=tk.W)
    name_entry = tk.Entry(details_frame)
    name_entry.grid(row=0, column=1, sticky=tk.EW)
    
    tk.Label(details_frame, text="Description:").grid(row=1, column=0, sticky=tk.W)
    desc_entry = tk.Entry(details_frame)
    desc_entry.grid(row=1, column=1, sticky=tk.EW)

    tk.Label(details_frame, text="Moisture Info:").grid(row=2, column=0, sticky=tk.W)
    moisture_entry = tk.Entry(details_frame)
    moisture_entry.grid(row=2, column=1, sticky=tk.EW)

    tk.Label(details_frame, text="Light/Temp Info:").grid(row=3, column=0, sticky=tk.W)
    light_entry = tk.Entry(details_frame)
    light_entry.grid(row=3, column=1, sticky=tk.EW)

    tk.Label(details_frame, text="Substrates:").grid(row=4, column=0, sticky=tk.W)
    substrates_entry = tk.Entry(details_frame)
    substrates_entry.grid(row=4, column=1, sticky=tk.EW)

    tk.Label(details_frame, text="Image Path:").grid(row=5, column=0, sticky=tk.W)
    image_entry = tk.Entry(details_frame)
    image_entry.grid(row=5, column=1, sticky=tk.EW)

    def update_entries(selected_plant):
        name_entry.delete(0, tk.END)
        name_entry.insert(0, selected_plant.plant_name)
        
        desc_entry.delete(0, tk.END)
        desc_entry.insert(0, selected_plant.plant_description)

        moisture_entry.delete(0, tk.END)
        moisture_entry.insert(0, selected_plant.moisture_info)

        light_entry.delete(0, tk.END)
        light_entry.insert(0, selected_plant.light_temp_info)

        substrates_entry.delete(0, tk.END)
        substrates_entry.insert(0, selected_plant.substrates)

        image_entry.delete(0, tk.END)
        image_entry.insert(0, selected_plant.image_path)

    def clear_entries():
        name_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)
        moisture_entry.delete(0, tk.END)
        light_entry.delete(0, tk.END)
        substrates_entry.delete(0, tk.END)
        image_entry.delete(0, tk.END)
        plant_listbox.selection_clear(0, tk.END) 

    def on_plant_select(event):
        selected_index = plant_listbox.curselection()
        if selected_index:
            selected_plant = plants[selected_index[0]]
            update_entries(selected_plant)

    plant_listbox.bind('<<ListboxSelect>>', on_plant_select)

    if plant:
        update_entries(plant)

    deselect_button = tk.Button(details_frame, text="Deselect", command=clear_entries)
    deselect_button.grid(row=6, column=0, columnspan=2, pady=10)

    def save_plant():
        from .gui_plants import initialize_plant_overview 
        name = name_entry.get()
        description = desc_entry.get()
        moisture_info = moisture_entry.get()
        light_temp_info = light_entry.get()
        substrates = substrates_entry.get()
        image_path = image_entry.get()

        if plant and not plant_listbox.curselection():
            update_plant(plant.plant_id, plant_name=name, plant_description=description,
                         moisture_info=moisture_info, light_temp_info=light_temp_info,
                         substrates=substrates, image_path=image_path)
        else:
            create_plant(name, image_path, description, moisture_info, light_temp_info, substrates)

        plant_window.destroy()
        initialize_plant_overview(parent_window, notebook) 

    save_button = tk.Button(details_frame, text="Save", command=save_plant)
    save_button.grid(row=7, column=0, columnspan=2, pady=10)

    def delete_plant_action():
        from .gui_plants import initialize_plant_overview

        selected_index = plant_listbox.curselection()
        if selected_index:
            selected_plant = plants[selected_index[0]]
            delete_plant(selected_plant.plant_id)
            plant_window.destroy()
            initialize_plant_overview(parent_window, notebook)

    delete_button = tk.Button(details_frame, text="Delete", command=delete_plant_action)
    delete_button.grid(row=8, column=0, columnspan=2, pady=10)
