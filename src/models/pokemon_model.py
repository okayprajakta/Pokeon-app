# src/models/pokemon_model.py
from sqlalchemy import Column, Integer, String, JSON
from src.config.database import Base

class Pokemon(Base):
    __tablename__ = "pokemons"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)  # ID is user-defined
    name = Column(String, nullable=False)  # Name of the Pokémon, cannot be null
    height = Column(Integer)  # Height of the Pokémon
    weight = Column(Integer)  # Weight of the Pokémon
    xp = Column(Integer)  # Experience points of the Pokémon
    image_url = Column(String)  # URL to the Pokémon's image
    pokemon_url = Column(String)  # URL to the Pokémon's details
    abilities = Column(JSON)  # JSON field to store the list of abilities
    stats = Column(JSON)  # JSON field to store the list of stats
    types = Column(JSON)  # JSON field to store the list of types