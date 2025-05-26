import openai
from sentence_transformers import SentenceTransformer

from app.configuration.config import Config
from app.configuration.model_type import ModelType

model_type = Config.MODEL_TYPE

def get_embedding(text: str) -> list[float]:
    if model_type == ModelType.CLOUD:
        return encode_by_cloud_model(text)
    else:
        return encode_by_local_model(text).tolist()

def encode_by_local_model(text):
    model = SentenceTransformer(Config.LOCAL_MODEL_EMBEDDER_NAME)
    return model.encode(text)

def encode_by_cloud_model(text):
    resp = openai.embeddings.create(
        model=Config.CLOUD_MODEL_EMBEDDER_NAME,
        input=text
    )
    return resp["data"][0]["embedding"]

def create_embedded_text(event):
    text_to_embed = f"{event.name} | {event.location} | {event.type} | at {event.time}"
    return get_embedding(text_to_embed)