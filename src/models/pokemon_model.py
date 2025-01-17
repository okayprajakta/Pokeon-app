from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Pokemon(Base):
    __tablename__ = 'pokemons'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    height = Column(Integer)
    weight = Column(Integer)
    xp = Column(Integer)
    image_url = Column(String, nullable=True)  # Ensure this is added
    pokemon_url = Column(String, nullable=False)
    abilities = Column(JSONB, nullable=False)
    stats = Column(JSONB, nullable=False)
    types = Column(JSONB, nullable=False)

    def __init__(self, id, name, height, weight, xp, pokemon_url, abilities, stats, types, image_url=None):
        self.id = id
        self.name = name
        self.height = height
        self.weight = weight
        self.xp = xp
        self.pokemon_url = pokemon_url
        self.abilities = abilities
        self.stats = stats
        self.types = types
        self.image_url = image_url  # This is the image_url parameter


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

