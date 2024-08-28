from domain.database import session
from domain.plants import Plant
from domain.user import User, get_user_by_username
from domain.sensor import Sensor, create_sensor
from domain.containers import Container, create_container
import random

def seed_data():
    # Seed plants data
    if session.query(Plant).count() == 0:
        plants_data = {
            "Acer": {
                "plant_name": "Acer",
                "plant_description": "Acer is a deciduous tree known for its colorful foliage. \nIt provides a source of maple syrup when tapped during the spring. \nAcer has a wide range of cultivars, \nincluding those with unique leaf shapes, \nsuch as the Japanese maple.",
                "moisture_info": "Acer requires consistent moisture to thrive.",
                "light_temp_info": "It prefers bright and warm conditions.",
                "substrates": "Well-draining soil is recommended for Acer.",
                "image_path": "images/acer.jpg"
            },
            "Anthurium": {
                "plant_name": "Anthurium",
                "plant_description": "Anthurium is a tropical plant that produces heart-shaped flowers. \nIt has a long blooming period, \nwith flowers lasting up to 8 weeks. \nAnthurium comes in a variety of colors, including pink, red, white, and orange.",
                "moisture_info": "Keep the soil consistently moist for Anthurium.",
                "light_temp_info": "Provide bright and warm conditions.",
                "substrates": "Use a well-draining potting mix for Anthurium.",
                "image_path": "images/anthurium.jpg"
            },
            "Bamboo": {
                "plant_name": "Bamboo",
                "plant_description": "Bamboo is a fast-growing grass used for construction and as food for animals. \nIt contains anti-bacterial and anti-inflammatory properties and \ncan absorb up to 12 tons of carbon dioxide per hectare, making it an effective tool against climate change.",
                "moisture_info": "Bamboo prefers consistently moist soil.",
                "light_temp_info": "It thrives in bright and warm conditions.",
                "substrates": "Bamboo does well in well-draining soil.",
                "image_path": "images/bamboo.jpg"
            },
            "Calla": {
                "plant_name": "Calla",
                "plant_description": "Calla is a perennial herb that produces trumpet-shaped flowers. \nIt symbolizes rebirth and resurrection and has medicinal uses, \nsuch as treatment for swelling and skin irritation.",
                "moisture_info": "Keep the soil consistently moist for Calla.",
                "light_temp_info": "Provide bright and warm conditions.",
                "substrates": "Well-draining soil is recommended for Calla.",
                "image_path": "images/calla.jpg"
            },
            "Davallia Fejeensis": {
                "plant_name": "Davallia Fejeensis",
                "plant_description": "Davallia Fejeensis is an epiphytic fern native to Fiji. \nIt is also known as the rabbit's foot fern due to its furry rhizomes. \nIt thrives in low-light environments and is easy to care for.",
                "moisture_info": "Keep the soil slightly moist for Davallia Fejeensis.",
                "light_temp_info": "It prefers low-light conditions.",
                "substrates": "Well-draining soil is suitable for this fern.",
                "image_path": "images/davallia_fejeensis.jpg"
            },
            "Dracena Marginata": {
                "plant_name": "Dracena Marginata",
                "plant_description": "Dracena Marginata is an evergreen tree with long, slender leaves with red edges. \nIt can grow up to 15 feet tall in optimal conditions and is air-purifying, removing toxins such as \nbenzene, formaldehyde, and trichloroethylene from the air.",
                "moisture_info": "Allow the soil to dry between waterings for Dracena Marginata.",
                "light_temp_info": "It prefers bright and warm conditions.",
                "substrates": "Use well-draining soil for this plant.",
                "image_path": "images/dracena_marginata.jpg"
            },
            "Epipremnum": {
                "plant_name": "Epipremnum",
                "plant_description": "Epipremnum is an epiphytic vine often used as a houseplant. \nIt can improve indoor air quality by removing pollutants such as formaldehyde, benzene, and xylene. \nIt has a unique variegated leaf pattern with shades of green, white, and yellow.",
                "moisture_info": "Keep the soil consistently moist for Epipremnum.",
                "light_temp_info": "It does well in bright and warm conditions.",
                "substrates": "Use a well-draining potting mix for Epipremnum.",
                "image_path": "images/epipremnum.jpg"
            },
            "Monstera Deliciosa": {
                "plant_name": "Monstera Deliciosa",
                "plant_description": "Monstera Deliciosa is a tropical vine that produces large, perforated leaves. \nIt symbolizes the pursuit of knowledge and a thirst for exploration. \nIt thrives in high humidity environments and is known for its adaptability to various light conditions.",
                "moisture_info": "Keep the soil slightly moist for Monstera Deliciosa.",
                "light_temp_info": "It can tolerate a range of light conditions, from bright to low light.",
                "substrates": "Well-draining soil is suitable for Monstera Deliciosa.",
                "image_path": "images/monstera_deliciosa.jpg"
            },
            "Pillea Elefantore": {
                "plant_name": "Pillea Elefantore",
                "plant_description": "Pillea Elefantore is a herbaceous perennial also known as the 'Chinese money plant.' \nIt symbolizes financial prosperity and good luck. \nIt thrives in well-draining soil and bright, indirect light.",
                "moisture_info": "Allow the soil to partially dry between waterings for Pillea Elefantore.",
                "light_temp_info": "It prefers bright, indirect light and moderate room temperatures.",
                "substrates": "Use a well-draining potting mix for this plant.",
                "image_path": "images/pillea_elefantore.jpg"
            },
            "Spatifilum": {
                "plant_name": "Spatifilum",
                "plant_description": "Spatifilum is a flowering plant that produces white or pink flowers. \nIt symbolizes peace and tranquility and is air-purifying, removing toxins such as \nbenzene, formaldehyde, and trichloroethylene from the air.",
                "moisture_info": "Keep the soil consistently moist for Spatifilum.",
                "light_temp_info": "It does well in low to moderate light conditions and prefers warmer temperatures.",
                "substrates": "Use well-draining soil for Spatifilum.",
                "image_path": "images/spatifilum.jpg"
            }
        }

        for plant in plants_data.values():
            new_plant = Plant(
                plant_name=plant["plant_name"],
                plant_description=plant["plant_description"],
                moisture_info=plant["moisture_info"],
                light_temp_info=plant["light_temp_info"],
                substrates=plant["substrates"],
                image_path=plant["image_path"]
            )
            session.add(new_plant)
        
        session.commit()

    if session.query(Container).count() == 0:
        first_plant = session.query(Plant).first()
        
        if first_plant:
            new_container = Container(
                container_material="Plastic",
                container_location="Living Room",
                plant_id=first_plant.plant_id
            )
            session.add(new_container)
            session.commit()

            create_sensor(
                container_id=new_container.container_id,
                sensor_type="light",
                light=random.uniform(0, 100),
                moisture=None,
                soil=None
            )
            create_sensor(
                container_id=new_container.container_id,
                sensor_type="moisture",
                moisture=random.uniform(0, 100),
                light=None,
                soil=None
            )
            create_sensor(
                container_id=new_container.container_id,
                sensor_type="soil",
                soil=random.uniform(5, 7.5),
                light=None,
                moisture=None
            )

        session.commit()

    # Seed a default user
    if not get_user_by_username(session, "Jura"):
        user = User(name="Jurica", surname="Barta", username="Jura", password="1234")
        session.add(user)
        session.commit()

if __name__ == "__main__":
    seed_data()
