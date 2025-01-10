from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Pokemon(Base):
    __tablename__ = "pokemons"  

    id = Column(Integer, primary_key=True, index=True, autoincrement=False) 
    name = Column(String, nullable=False)  
    height = Column(Integer)  
    weight = Column(Integer)  
    xp = Column(Integer) 
    image_url = Column(String)  
    pokemon_url = Column(String)  
    abilities = Column(JSON)  
    stats = Column(JSON) 
    types = Column(JSON)  


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

