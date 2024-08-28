from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from domain.database import Base, session

class Container(Base):
    __tablename__ = "containers"

    container_id = Column(Integer, primary_key=True, autoincrement=True)
    container_material = Column(String)
    container_location = Column(String, nullable=False)
    is_empty = Column(Boolean, default=True)
    plant_id = Column(Integer, ForeignKey('plants.plant_id'))

    plant = relationship('Plant')

    def __init__(self, container_material, container_location, plant_id=None):
        self.container_location = container_location
        self.container_material = container_material
        self.plant_id = plant_id
        self.is_empty = plant_id is None

def create_container(container_material, container_location, plant_id=None):
    new_container = Container(container_material, container_location, plant_id)
    session.add(new_container)
    session.commit()
    return new_container

def get_container_by_id(container_id):
    return session.query(Container).filter(Container.container_id == container_id).first()

def get_all_containers():
    return session.query(Container).all()

def update_container(container_id, **kwargs):
    container = session.query(Container).filter(Container.container_id == container_id).first()
    if container:
        for key, value in kwargs.items():
            setattr(container, key, value)
        # Update is_empty based on the plant_id
        if 'plant_id' in kwargs:
            container.is_empty = kwargs['plant_id'] == 0
        session.commit()
        return container
    return None

def delete_container(container_id):
    container = session.query(Container).filter(Container.container_id == container_id).first()
    if container:
        session.delete(container)
        session.commit()
        return container
    return None