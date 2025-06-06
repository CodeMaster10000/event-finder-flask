import os
from pathlib import Path
from dotenv import load_dotenv
from app.configuration.model_type import ModelType


PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")

def get_model_type(model_type: str) -> ModelType:
    if model_type.lower() == "local":
        return ModelType.LOCAL
    else:
        return ModelType.CLOUD

class Config:
    DB_NAME = os.environ.get("DB_NAME", "events_db")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    VECTOR_DIM = int(os.environ.get("VECTOR_DIM", "1536"))
    CLOUD_MODEL_API_KEY = os.environ.get("MODEL_API_KEY")
    CLOUD_MODEL_EMBEDDER_NAME=os.environ.get("CLOUD_MODEL_EMBEDDER_NAME", "text-embedding-ada-002")
    MODEL_TYPE = get_model_type(os.environ.get("MODEL_TYPE", ModelType.LOCAL.value))
    LOCAL_MODEL_NAME = os.environ.get("LOCAL_MODEL_NAME", "llama3.2-vision")
    LOCAL_MODEL_EMBEDDER_NAME = os.environ.get("LOCAL_MODEL_EMBEDDER_NAME", "sentence-transformers/all-mpnet-base-v2")
    NUMBER_OF_EVENTS_TO_SEARCH= os.environ.get("NUMBER_OF_EVENTS_TO_SEARCH", 5)
    CLOUD_MODEL_NAME=os.environ.get("CLOUD_MODEL_NAME", "gpt-4")
    CLOUD_MODEL_TEMPERATURE=os.environ.get("CLOUD_MODEL_TEMPERATURE", 0.7)
    CLOUD_MODEL_MAX_TOKENS=os.environ.get("CLOUD_MODEL_MAX_TOKENS", 500)