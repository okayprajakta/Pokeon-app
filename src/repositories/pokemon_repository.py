from sqlalchemy.orm import Session
from src.models.pokemon_model import Pokemon
from src.schemas.pokemon_schema import PokemonCreate, PokemonUpdate, PokemonBase  # Updated import path
from fastapi import HTTPException, status

def get_pokemon(db: Session, pokemon_id: int):
    """Retrieve a Pokémon by its ID."""
    return db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()

def get_all_pokemon(db: Session, skip: int = 0, limit: int = 100, name: str = None, min_height: int = None, max_height: int = None, min_weight: int = None, max_weight: int = None):
    """Retrieve all Pokémon with optional filters and pagination."""
    query = db.query(Pokemon)
    
    if name:
        query = query.filter(Pokemon.name.ilike(f"%{name}%"))
    if min_height is not None:
        query = query.filter(Pokemon.height >= min_height)
    if max_height is not None:
        query = query.filter(Pokemon.height <= max_height)
    if min_weight is not None:
        query = query.filter(Pokemon.weight >= min_weight)
    if max_weight is not None:
        query = query.filter(Pokemon.weight <= max_weight)
    
    return query.offset(skip).limit(limit).all()

def create_pokemon(db: Session, pokemon: PokemonCreate):
    """Create a new Pokémon."""
    existing_pokemon = get_pokemon(db, pokemon.id)
    if existing_pokemon:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pokemon already exists")
    db_pokemon = Pokemon(**pokemon.dict())
    db.add(db_pokemon)  # Add the Pokémon to the session
    db.commit()  # Commit the transaction
    db.refresh(db_pokemon)  # Refresh the instance with the latest data from the database
    return db_pokemon  # Return the created Pokémon

def update_pokemon(db: Session, pokemon_id: int, pokemon: PokemonUpdate):
    """Update an existing Pokémon."""
    db_pokemon = db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    if db_pokemon:
        for key, value in pokemon.dict(exclude_unset=True).items():
            setattr(db_pokemon, key, value)  # Update the Pokémon's attributes
        db.commit()  # Commit the transaction
        db.refresh(db_pokemon)  # Refresh the instance with the latest data from the database
    return db_pokemon  # Return the updated Pokémon

def delete_pokemon(db: Session, pokemon_id: int):
    """Delete a Pokémon by its ID."""
    db_pokemon = db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    if db_pokemon:
        db.delete(db_pokemon)  # Delete the Pokémon from the session
        db.commit()  # Commit the transaction
    return db_pokemon  # Return the deleted Pokémon