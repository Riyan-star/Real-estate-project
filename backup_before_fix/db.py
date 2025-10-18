import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ensure we load .env from the project root (where this file lives)
root = Path(__file__).resolve().parent
env_path = root / '.env'
# If not found next to db.py, try parent directory
if not env_path.exists():
    env_path = root.parent / '.env'
# If still not found, load_dotenv will just do nothing (we keep defaults)
load_dotenv(dotenv_path=str(env_path) if env_path.exists() else None)

PGUSER = os.getenv("PGUSER", "postgres")
PGPASSWORD = os.getenv("PGPASSWORD", "")
PGHOST = os.getenv("PGHOST", "localhost")
PGPORT = os.getenv("PGPORT", "5432")
PGDATABASE = os.getenv("PGDATABASE", "realestate_db")

DATABASE_URL = f"postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"

# Engine and session
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()

def get_session():
    return SessionLocal()
