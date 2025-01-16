#src/main.py
from fastapi import FastAPI
from src.routers import pokemon_router, auth_router
# from src.models.pokemon_model import Base as PokemonBase
# from src.models.user_model import Base as UserBase
# from src.config.database import engine


app = FastAPI()

# # Create all tables in the database
# PokemonBase.metadata.create_all(bind=engine)
# UserBase.metadata.create_all(bind=engine)

# Include authentication and Pokémon routers
app.include_router(auth_router.router, tags=["Authentication"])
app.include_router(pokemon_router.router, tags=["Pokémon"])

