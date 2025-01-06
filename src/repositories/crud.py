# src/repositories/crud.py
from sqlalchemy.orm import Session
from src.models.pokemon_model import Pokemon
from src.schemas.pokemon_schema import PokemonCreate, PokemonUpdate

def create_pokemon(db: Session, pokemon: PokemonCreate):
    # db_pokemon = Pokemon(**pokemon.dict())
    db_pokemon = Pokemon(**pokemon)
    db.add(db_pokemon)
    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon

def get_pokemon(db: Session, pokemon_id: int):
    return db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()

def get_pokemons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pokemon).offset(skip).limit(limit).all()

def update_pokemon(db: Session, pokemon_id: int, pokemon: PokemonUpdate):
    db_pokemon = db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    if not db_pokemon:
        return None
    update_data = pokemon.dict(exclude_unset=True)  # Exclude fields not provided
    update_data.pop("id", None)  # Prevent the `id` field from being updated
    for key, value in update_data.items():
        setattr(db_pokemon, key, value)
    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon

def delete_pokemon(db: Session, pokemon_id: int):
    db_pokemon = db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    if db_pokemon:
        db.delete(db_pokemon)
        db.commit()
        return db_pokemon
    return None
