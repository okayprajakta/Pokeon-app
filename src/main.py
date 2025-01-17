from fastapi import FastAPI
from src.routers import pokemon_router, auth_router

app = FastAPI()

app.include_router(auth_router.router, tags=["Authentication"])
app.include_router(pokemon_router.router, tags=["Pokémon"])

