from src.config.database import engine
from src.models.pokemon_model import Pokemon
from src.models.user_model import User

# Create all tables in the database
# src.models.pokemon_model.Base.metadata.create_all(bind=engine)

# Create all tables in the database
Pokemon.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)