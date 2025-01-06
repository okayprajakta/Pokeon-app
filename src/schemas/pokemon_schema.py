# src/schemas/pokemon_schema.py
from pydantic import BaseModel
from typing import List, Optional

class Ability(BaseModel):
    name: str
    is_hidden: bool

class Stat(BaseModel):
    name: str
    base_stat: int

class Type(BaseModel):
    name: str

class PokemonBase(BaseModel):
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

class PokemonCreate(PokemonBase):
    id: Optional[int]  # Allow user to provide an ID during creation
    name: str          # Make `name` mandatory for creation
    height: int
    weight: int
    xp: int
    image_url: str
    pokemon_url: str
    abilities: List[Ability]
    stats: List[Stat]
    types: List[Type]

class PokemonUpdate(BaseModel):
    name: str          # Make `name` mandatory for creation
    height: int
    weight: int
    xp: int
    image_url: str
    pokemon_url: str
    abilities: List[Ability]
    stats: List[Stat]
    types: List[Type]



class Pokemon(PokemonBase):
    id: int  # ID is mandatory in the response

    class Config:
        from_attributes = True
