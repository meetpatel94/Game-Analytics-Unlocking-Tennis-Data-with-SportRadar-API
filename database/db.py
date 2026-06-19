import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def get_engine():
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise ValueError(
            "DATABASE_URL not found. Check .env file."
        )

    return create_engine(db_url)