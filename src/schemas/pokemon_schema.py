#src/schemas/pokemon_schema.py
from pydantic import BaseModel
from typing import List, Optional

class Ability(BaseModel):
    """Schema for Pokémon abilities."""
    name: str
    is_hidden: bool

class Stat(BaseModel):
    """Schema for Pokémon stats."""
    name: str
    base_stat: int

class Type(BaseModel):
    """Schema for Pokémon types."""
    name: str

class PokemonBase(BaseModel):
    """Base schema for Pokémon with optional fields."""
    id: int
    name: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    xp: Optional[int] = None
    image_url: Optional[str] = None
    pokemon_url: Optional[str] = None
    abilities: Optional[List[Ability]] = None
    stats: Optional[List[Stat]] = None
    types: Optional[List[Type]] = None

class PokemonCreate(BaseModel):
    """Schema for creating a new Pokémon."""
    id: Optional[int]  # Allow user to provide an ID during creation
    name: str          # Make `name` mandatory for creation
    height: int
    weight: int
    xp: int
    image_url: Optional[str] = None  # Make sure this matches the model field
    pokemon_url: str
    abilities: List[Ability]
    stats: List[Stat]
    types: List[Type]

class PokemonUpdate(BaseModel):
    """Schema for updating an existing Pokémon."""
    name: Optional[str] = None          
    height: Optional[int] = None
    weight: Optional[int] = None
    xp:   Optional[int] = None
    image_url: Optional[str] = None
    pokemon_url: Optional[str] = None
    abilities: Optional[List[Ability]] = None 
    stats: Optional[List[Stat]] = None
    types: Optional[List[Type]] = None

class Pokemon(PokemonBase):
    """Schema for Pokémon response with mandatory ID."""
    id: int  # ID is mandatory in the response

    class Config:
        from_attributes = True  # Enable ORM mode
