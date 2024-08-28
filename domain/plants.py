from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from domain.database import Base, session

class Plant(Base):
    __tablename__ = "plants"

    plant_id = Column(Integer, primary_key=True, autoincrement=True)
    plant_name = Column(String, nullable=False)
    plant_description = Column(String)  
    moisture_info = Column(String)  
    light_temp_info = Column(String)  
    substrates = Column(String)  
    image_path = Column(String)

    def __init__(self, plant_name, image_path, plant_description = "", moisture_info = "", light_temp_info = "", substrates = ""):
        self.plant_name = plant_name
        self.plant_description = plant_description
        self.moisture_info = moisture_info
        self.light_temp_info = light_temp_info
        self.substrates = substrates
        self.image_path = image_path

def create_plant(plant_name, image_path, plant_desc="", moisture_info="", light_temp_info="", substrates=""):
    new_plant = Plant(plant_name, image_path, plant_desc, moisture_info, light_temp_info, substrates)
    session.add(new_plant)
    session.commit()
    return new_plant

def get_plant_by_id(plant_id):
    return session.query(Plant).filter(Plant.plant_id == plant_id).first()

def get_all_plants():
    return session.query(Plant).all()

def update_plant(plant_id, **kwargs):
    plant = session.query(Plant).filter(Plant.plant_id == plant_id).first()
    if plant:
        for key, value in kwargs.items():
            setattr(plant, key, value)
        session.commit()
        return plant
    return None

def delete_plant(plant_id):
    plant = session.query(Plant).filter(Plant.plant_id == plant_id).first()
    if plant:
        session.delete(plant)
        session.commit()
        return plant
    return None