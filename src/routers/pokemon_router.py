import os
from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile, Form, Response
from sqlalchemy.orm import Session
from src.repositories.pokemon_repository import create_pokemon, get_pokemon, get_all_pokemon, update_pokemon, delete_pokemon
from src.schemas.pokemon_schema import PokemonCreate, Pokemon, PokemonBase
from typing import List, Optional
from src.config.database import SessionLocal
from src.middleware.auth_middleware import JWTBearer
import json
from src.config.aws_s3 import upload_to_s3, validate_image_file
from dotenv import load_dotenv

load_dotenv()  

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
    abilities: str = Form(..., description='Example: [{"name": "Static", "is_hidden": false}, {"name": "Lightning Rod", "is_hidden": true}]'),  
    stats: str = Form(..., description='Example: [{"name": "Speed", "base_stat": 90}, {"name": "Attack", "base_stat": 55}]'), 
    types: str = Form(..., description='Example: [{"name": "Electric"}]'),  
    db: Session = Depends(get_db),
    image: Optional[UploadFile] = File(None)  
):
    """
    Endpoint to create a new Pokémon.
    Users can specify their own ID or let it be auto-generated.
    """
    abilities = json.loads(abilities)
    stats = json.loads(stats)
    types = json.loads(types)

    # Handle the image file if provided
    default_image_url = f"https://pokeres.bastionbot.org/images/{name}.png"  
    image_url = default_image_url
    if image and image.filename:
        validate_image_file(image)
        object_name = f"images/{image.filename}"
        bucket_name = os.getenv("S3_BUCKET_NAME")
        if not bucket_name:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="S3 bucket name is not set.")
        image_url = upload_to_s3(image, bucket_name, object_name)

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
        image_url=image_url  
    )

    return create_pokemon(db=db, pokemon=pokemon)

@router.get("/pokemon/{pokemon_id}", response_model=Pokemon, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_pokemon_endpoint(pokemon_id: int, db: Session = Depends(get_db), response: Response = None):
    """
    Endpoint to retrieve a Pokémon by ID.
    """
    db_pokemon = get_pokemon(db, pokemon_id)
    if db_pokemon is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokemon not found")
    return db_pokemon

@router.get("/pokemon/", response_model=List[PokemonBase], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_all_pokemon_endpoint(
    skip: Optional[int] = None,
    limit: Optional[int] = None,
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
    image: Optional[UploadFile] = File(None)  
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