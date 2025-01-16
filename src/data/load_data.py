#src/data/load_data.py
import json
from sqlalchemy.orm import Session
from src.models.pokemon_model import Pokemon
from src.repositories.crud import create_pokemon, update_pokemon

def load_pokemon_data(db: Session):
    # Load Pokémon data from JSON file
    with open('src/data/pokedex_raw_array.json') as f:
        pokemon_data = json.load(f)

        for item in pokemon_data:
            # Create a dictionary for Pokémon data
            pokemon_data_dict = {
                "id": item["id"],
                "name": item["name"],
                "height": item.get("height"),
                "weight": item.get("weight"),
                "xp": item.get("xp"),
                "image_url": item.get("image_url"),
                "pokemon_url": item.get("pokemon_url"),
                "abilities": item.get("abilities", []),
                "stats": item.get("stats", []),
                "types": item.get("types", [])
            }
            # Check if Pokémon already exists
            existing_pokemon = db.query(Pokemon).filter(Pokemon.id == item["id"]).first()
            if existing_pokemon:
                pass 
            else:
                # Create new Pokémon
                create_pokemon(db=db, pokemon=pokemon_data_dict) 

if __name__ == "__main__":
    from src.config.database import SessionLocal

    # Initialize the database session
    db = SessionLocal()
    try:
        load_pokemon_data(db)
        print("Data loaded successfully.")
    finally:
        db.close()