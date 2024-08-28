from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from domain.database import Base, session

class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_type = Column(String, nullable=False)
    moisture = Column(Float, nullable=True)
    light = Column(Float, nullable=True)
    soil = Column(Float, nullable=True)
    
    container_id = Column(Integer, ForeignKey('containers.container_id'), nullable=False)
    
    container = relationship("Container")

    def __init__(self, sensor_type, container_id, moisture = None, light = None, soil = None):
        self.sensor_type = sensor_type
        self.moisture = moisture
        self.light = light
        self.soil = soil
        self.container_id = container_id

def create_sensor(sensor_type, container_id, moisture=None, light=None, soil=None):
    if sensor_type == "light":
        moisture = 0.0 if moisture is None else moisture  
        soil = 0.0 if soil is None else soil             
    elif sensor_type == "moisture":
        light = 0.0 if light is None else light           
        soil = 0.0 if soil is None else soil             
    elif sensor_type == "soil":
        light = 0.0 if light is None else light           
        moisture = 0.0 if moisture is None else moisture  

    new_sensor = Sensor(sensor_type=sensor_type, container_id=container_id, moisture=moisture, light=light, soil=soil)
    session.add(new_sensor)
    session.commit()
    return new_sensor

def get_sensor_by_id(sensor_id):
    return session.query(Sensor).filter(Sensor.id == sensor_id).first()

def get_all_sensors():
    return session.query(Sensor).all()

def update_sensor(sensor_id, **kwargs):
    sensor = session.query(Sensor).filter(Sensor.id == sensor_id).first()
    if sensor:
        for key, value in kwargs.items():
            setattr(sensor, key, value)
        session.commit()
        return sensor
    return None

def delete_sensor(sensor_id):
    sensor = session.query(Sensor).filter(Sensor.id == sensor_id).first()
    if sensor:
        session.delete(sensor)
        session.commit()
        return sensor
    return None