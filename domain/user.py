from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from domain.database import Base, session

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    
    def __init__(self, name, surname, username, password):
        self.name = name
        self.surname = surname
        self.username = username
        self.password = password

def create_user(session, name, surname, username, password):
    user = User(name=name, surname=surname, username=username, password=password)
    session.add(user)
    session.commit()
    return user

def get_user_by_id(session, user_id):
    return session.query(User).filter(User.user_id == user_id).first()

def get_user_by_username(session, username):
    return session.query(User).filter(User.username == username).first()

def get_all_users(session):
    return session.query(User).all()

def update_user(session, user_id, **kwargs):
    user = session.query(User).filter(User.user_id == user_id).first()
    if user:
        for key, value in kwargs.items():
            setattr(user, key, value)
        session.commit()
        return user
    return None

def delete_user(session, user_id):
    user = session.query(User).filter(User.user_id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
        return user
    return None