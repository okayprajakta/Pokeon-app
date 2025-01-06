from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from src.repositories.pokemon_repository import create_pokemon, get_pokemon, get_all_pokemon, update_pokemon, delete_pokemon
from src.schemas.pokemon_schema import PokemonCreate, PokemonUpdate, Pokemon, PokemonBase  # Updated import
from typing import List, Optional
from src.config.database import SessionLocal

router = APIRouter()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pokemon/", response_model=Pokemon, status_code=status.HTTP_201_CREATED)
def create_pokemon_endpoint(pokemon: PokemonCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new Pokémon. 
    Users can specify their own ID or let it be auto-generated.
    """
    return create_pokemon(db=db, pokemon=pokemon)

@router.get("/pokemon/{pokemon_id}", response_model=Pokemon, status_code=status.HTTP_200_OK)
def get_pokemon_endpoint(pokemon_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a Pokémon by ID.
    """
    print("passing..............")
    db_pokemon = get_pokemon(db, pokemon_id)

    print("db_pokemon -->", db_pokemon)
    if db_pokemon is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokemon not found")
    return db_pokemon

@router.get("/pokemon/", response_model=List[PokemonBase], status_code=status.HTTP_200_OK)
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

@router.patch("/pokemon/{pokemon_id}", response_model=Pokemon, status_code=status.HTTP_200_OK)
def update_pokemon_endpoint(pokemon_id: int, pokemon: PokemonUpdate, db: Session = Depends(get_db)):
    """
    Endpoint to partially update a Pokémon.
    ID updates are explicitly disallowed.
    """
    db_pokemon = update_pokemon(db, pokemon_id, pokemon)
    if db_pokemon is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokemon not found")
    return db_pokemon

@router.delete("/pokemon/{pokemon_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pokemon_endpoint(pokemon_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to delete a Pokémon by ID.
    """
    db_pokemon = delete_pokemon(db, pokemon_id)
    if db_pokemon is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokemon not found")
    return None