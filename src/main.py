from fastapi import FastAPI
from src.routers import pokemon_router  # Ensure correct import
from src.models.pokemon_model import Base
from src.config.database import engine
from src.data.load_data import load_pokemon_data
from src.config.database import SessionLocal

app = FastAPI()

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Load Pokémon data into the database
load_pokemon_data(db=SessionLocal())

# Include the Pokémon router
app.include_router(pokemon_router.router, tags=["Pokémon"])