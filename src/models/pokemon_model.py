# src/models/pokemon_model.py
from sqlalchemy import Column, Integer, String, JSON
from src.config.database import Base

class Pokemon(Base):
    __tablename__ = "pokemons"

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)  # ID is user-defined
    name = Column(String, nullable=False)
    height = Column(Integer)
    weight = Column(Integer)
    xp = Column(Integer)
    image_url = Column(String)
    pokemon_url = Column(String)
    abilities = Column(JSON)  # JSON field to store the list of abilities
    stats = Column(JSON)      # JSON field to store the list of stats
    types = Column(JSON)      # JSON field to store the list of types
