from src.config.database import engine
import src.models.pokemon_model

# Create all tables in the database
src.models.pokemon_model.Base.metadata.create_all(bind=engine)