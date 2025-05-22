import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    VECTOR_DIM = int(os.environ.get("VECTOR_DIM", "1536"))