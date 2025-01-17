from sqlalchemy.orm import Session
from src.models.pokemon_model import Pokemon
from src.schemas.pokemon_schema import PokemonCreate, PokemonUpdate, PokemonBase
from fastapi import HTTPException, status, UploadFile
from typing import Optional
from src.config.aws_s3 import upload_to_s3, validate_image_file
import os
import json

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
    existing_pokemon = db.query(Pokemon).filter(Pokemon.id == pokemon.id).first()
    if existing_pokemon:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pokemon already exists")
    
    # Convert Ability, Stat, and Type objects to dictionaries
    abilities = [ability.dict() for ability in pokemon.abilities]
    stats = [stat.dict() for stat in pokemon.stats]
    types = [type_.dict() for type_ in pokemon.types]
    
    db_pokemon = Pokemon(
        id=pokemon.id,
        name=pokemon.name,
        height=pokemon.height,
        weight=pokemon.weight,
        xp=pokemon.xp,
        pokemon_url=pokemon.pokemon_url,
        abilities=abilities,
        stats=stats,
        types=types,
        image_url=pokemon.image_url  # Make sure this is image_url
    )
    
    db.add(db_pokemon)  
    db.commit()  
    db.refresh(db_pokemon)  
    return db_pokemon

def update_pokemon(db: Session, pokemon_id: int, name: Optional[str], height: Optional[int], weight: Optional[int], xp: Optional[int], pokemon_url: Optional[str], abilities: Optional[str], stats: Optional[str], types: Optional[str], image: Optional[UploadFile]):
    """Update an existing Pokémon."""
    db_pokemon = db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    if db_pokemon:
        # Handle the image file if provided
        if image and image.filename:
            validate_image_file(image)
            object_name = f"images/{image.filename}"
            image_url = upload_to_s3(image.file, os.getenv("S3_BUCKET_NAME"), object_name)
            setattr(db_pokemon, 'image_url', image_url)

        # Update other fields
        update_data = {
            "name": name,
            "height": height,
            "weight": weight,
            "xp": xp,
            "pokemon_url": pokemon_url,
            "abilities": json.loads(abilities) if abilities else None,
            "stats": json.loads(stats) if stats else None,
            "types": json.loads(types) if types else None
        }

        for key, value in update_data.items():
            if value is not None:
                setattr(db_pokemon, key, value)
        
        db.commit()
        db.refresh(db_pokemon)
    return db_pokemon

def delete_pokemon(db: Session, pokemon_id: int):
    """Delete a Pokémon by its ID."""
    db_pokemon = db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    if db_pokemon:
        db.delete(db_pokemon)  
        db.commit()  
    return db_pokemon
