import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

db_config = {
    "host": os.getenv("NETFLIX_DB_HOST"),
    "database": os.getenv("NETFLIX_DB_NAME"),
    "user": os.getenv("NETFLIX_DB_USER"),
    "password": os.getenv("NETFLIX_DB_PASSWORD"),
}
