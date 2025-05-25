import psycopg2
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")
    result = urlparse(database_url)
    return psycopg2.connect(
        dbname= result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )
