#src/routers/pokemon_router.py
import os
from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile, Form
from sqlalchemy.orm import Session
from src.repositories.pokemon_repository import create_pokemon, get_pokemon, get_all_pokemon, update_pokemon, delete_pokemon
from src.schemas.pokemon_schema import PokemonCreate, PokemonUpdate, Pokemon, PokemonBase
from typing import List, Optional
from src.config.database import SessionLocal
from src.middleware.auth_middleware import JWTBearer
from src.config.aws_s3 import upload_to_s3
import json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pokemon/", response_model=Pokemon, status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
def create_pokemon_endpoint(
    id: int = Form(...),
    name: str = Form(...),
    height: int = Form(...),
    weight: int = Form(...),
    xp: int = Form(...),
    pokemon_url: str = Form(...),
    abilities: str = Form(...),  # JSON string
    stats: str = Form(...),  # JSON string
    types: str = Form(...),  # JSON string
    db: Session = Depends(get_db),
    image: Optional[UploadFile] = File(None)  # Image file
):
    """
    Endpoint to create a new Pokémon.
    Users can specify their own ID or let it be auto-generated.
    """
    # Parse JSON strings into Python objects
    abilities = json.loads(abilities)
    stats = json.loads(stats)
    types = json.loads(types)

    # Handle the image file if provided
    image_url = None
    if image and image.filename:
        object_name = f"images/{image.filename}"
        image_url = upload_to_s3(image.file, os.getenv("S3_BUCKET_NAME"), object_name)

    # Create PokemonCreate object
    pokemon = PokemonCreate(
        id=id,
        name=name,
        height=height,
        weight=weight,
        xp=xp,
        pokemon_url=pokemon_url,
        abilities=abilities,
        stats=stats,
        types=types,
        image_url=image_url  # Store the image URL here
    )

    return create_pokemon(db=db, pokemon=pokemon)

@router.get("/pokemon/{pokemon_id}", response_model=Pokemon, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_pokemon_endpoint(pokemon_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a Pokémon by ID.
    """
    db_pokemon = get_pokemon(db, pokemon_id)

    if db_pokemon is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokemon not found")
    return db_pokemon

@router.get("/pokemon/", response_model=List[PokemonBase], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_all_pokemon_endpoint(
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = Query(None, description="Filter by name"),
    min_height: Optional[int] = Query(None, description="Filter by minimum height"),
    max_height: Optional[int] = Query(None, description="Filter by maximum height"),
    min_weight: Optional[int] = Query(None, description="Filter by minimum weight"),
    max_weight: Optional[int] = Query(None, description="Filter by maximum weight"),
    db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve all Pokémon with optional filtering.
    """
    return get_all_pokemon(
        db, 
        skip=skip, 
        limit=limit, 
        name=name, 
        min_height=min_height, 
        max_height=max_height, 
        min_weight=min_weight, 
        max_weight=max_weight
    )

@router.patch("/pokemon/{pokemon_id}", response_model=Pokemon, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def update_pokemon_endpoint(pokemon_id: int, pokemon: PokemonUpdate, db: Session = Depends(get_db)):
    """
    Endpoint to partially update a Pokémon.
    ID updates are explicitly disallowed.
    """
    db_pokemon = update_pokemon(db, pokemon_id, pokemon)
    if db_pokemon is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokemon not found")
    return db_pokemon

@router.delete("/pokemon/{pokemon_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(JWTBearer())])
def delete_pokemon_endpoint(pokemon_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to delete a Pokémon by ID.
    """
    db_pokemon = delete_pokemon(db, pokemon_id)
    if db_pokemon is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokemon not found")
    return None
