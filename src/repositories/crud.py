# src/repositories/crud.py
from sqlalchemy.orm import Session
from src.models.pokemon_model import Pokemon
from src.schemas.pokemon_schema import PokemonCreate, PokemonUpdate

def create_pokemon(db: Session, pokemon: PokemonCreate):
    # Create a new Pokémon instance
    # db_pokemon = Pokemon(**pokemon.dict())
    db_pokemon = Pokemon(**pokemon)
    db.add(db_pokemon)  # Add the Pokémon to the session
    db.commit()  # Commit the transaction
    db.refresh(db_pokemon)  # Refresh the instance with the latest data from the database
    return db_pokemon  # Return the created Pokémon

def get_pokemon(db: Session, pokemon_id: int):
    # Retrieve a Pokémon by its ID
    return db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()

def get_pokemons(db: Session, skip: int = 0, limit: int = 100):
    # Retrieve a list of Pokémon with pagination
    return db.query(Pokemon).offset(skip).limit(limit).all()

def update_pokemon(db: Session, pokemon_id: int, pokemon: PokemonUpdate):
    # Update an existing Pokémon
    db_pokemon = db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    if not db_pokemon:
        return None  # Pokémon not found
    update_data = pokemon.dict(exclude_unset=True)  # Exclude fields not provided
    update_data.pop("id", None)  # Prevent the `id` field from being updated
    for key, value in update_data.items():
        setattr(db_pokemon, key, value)  # Update the Pokémon's attributes
    db.commit()  # Commit the transaction
    db.refresh(db_pokemon)  # Refresh the instance with the latest data from the database
    return db_pokemon  # Return the updated Pokémon

def delete_pokemon(db: Session, pokemon_id: int):
    # Delete a Pokémon by its ID
    db_pokemon = db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    if db_pokemon:
        db.delete(db_pokemon)  # Delete the Pokémon from the session
        db.commit()  # Commit the transaction
        return db_pokemon  # Return the deleted Pokémon
    return None  # Pokémon not found