import os
from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile, Form, Response
from sqlalchemy.orm import Session
from src.repositories.pokemon_repository import create_pokemon, get_pokemon, get_all_pokemon, update_pokemon, delete_pokemon
from src.schemas.pokemon_schema import PokemonCreate, PokemonUpdate, Pokemon, PokemonBase, Ability
from typing import List, Optional
from src.config.database import SessionLocal
from src.middleware.auth_middleware import JWTBearer
import json
from src.config.aws_s3 import upload_to_s3, validate_image_file, check_image_exists_in_s3
from urllib.parse import urlparse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/pokemon/", response_model=Pokemon, status_code=status.HTTP_201_CREATED)#, dependencies=[Depends(JWTBearer())])
def create_pokemon_endpoint(
    id: int = Form(...),
    name: str = Form(...),
    height: int = Form(...),
    weight: int = Form(...),
    xp: int = Form(...),
    pokemon_url: str = Form(...),
    abilities: str = Form(..., description='Example: [{"name": "Static", "is_hidden": false}, {"name": "Lightning Rod", "is_hidden": true}]'),  # JSON string
    stats: str = Form(..., description='Example: [{"name": "Speed", "base_stat": 90}, {"name": "Attack", "base_stat": 55}]'),  # JSON string
    types: str = Form(..., description='Example: [{"name": "Electric"}]'),  # JSON string
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
    # Handle the image file if provided
    default_image_url = f"https://pokeres.bastionbot.org/images/{name}.png"  # Customize the default image URL
    image_url = default_image_url
    if image and image.filename:
        validate_image_file(image)
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

@router.get("/pokemon/{pokemon_id}", response_model=Pokemon, status_code=status.HTTP_200_OK)
def get_pokemon_endpoint(pokemon_id: int, db: Session = Depends(get_db), response: Response = None):
    """
    Endpoint to retrieve a Pokémon by ID.
    """
    db_pokemon = get_pokemon(db, pokemon_id)

    if db_pokemon is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokemon not found")

    message = "Image exists in S3 bucket."

    # Check if the Pokémon has an image URL
    if db_pokemon.image_url:
        bucket_name = os.getenv("S3_BUCKET_NAME")

        # Check if the image URL contains the S3 bucket name
        if bucket_name in db_pokemon.image_url:
            message = "This Pokémon has an image in the S3 bucket."
        else:
            message = "This Pokémon has an image URL but it doesn't have any image in the S3 bucket."
    else:
        message = "This Pokémon doesn't have any image URL."

    # Set response headers
    response.headers["X-Image-URL"] = db_pokemon.image_url if db_pokemon.image_url else "No image URL"
    response.headers["X-Message"] = message

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

@router.patch("/pokemon/{pokemon_id}", response_model=Pokemon, status_code=status.HTTP_200_OK)#, dependencies=[Depends(JWTBearer())])
def update_pokemon_endpoint(
    pokemon_id: int,
    name: Optional[str] = Form(None),
    height: Optional[int] = Form(None),
    weight: Optional[int] = Form(None),
    xp: Optional[int] = Form(None),
    pokemon_url: Optional[str] = Form(None),
    abilities: Optional[str] = Form(None, description='Example: [{"name": "Static", "is_hidden": false}, {"name": "Lightning Rod", "is_hidden": true}]'),  # JSON string
    stats: Optional[str] = Form(None, description='Example: [{"name": "Speed", "base_stat": 90}, {"name": "Attack", "base_stat": 55}]'),  # JSON string
    types: Optional[str] = Form(None, description='Example: [{"name": "Electric"}]'),  # JSON string
    db: Session = Depends(get_db),
    image: Optional[UploadFile] = File(None)  # Image file
):
    """
    Endpoint to partially update a Pokémon.
    ID updates are explicitly disallowed.
    """
    db_pokemon = update_pokemon(db, pokemon_id, name, height, weight, xp, pokemon_url, abilities, stats, types, image)
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
