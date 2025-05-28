from sentence_transformers import SentenceTransformer

from app.configuration.config import Config
from app.configuration.model_type import ModelType
from app.error_handler.exceptions import ModelException

model_type = Config.MODEL_TYPE

def get_embedding(text: str) -> list[float]:
    if model_type == ModelType.CLOUD:
        return encode_by_cloud_model(text)
    else:
        return encode_by_local_model(text)

def encode_by_local_model(text):
   try:
       model = SentenceTransformer(Config.LOCAL_MODEL_EMBEDDER_NAME)
       return model.encode(text).tolist()
   except Exception as e:
       raise ModelException(f"Error while encoding using SentenceTransformer: {e}", 500) from e

def encode_by_cloud_model(text):
    # try:
    #     resp = openai.embeddings.create(
    #         model=Config.CLOUD_MODEL_EMBEDDER_NAME,
    #         input=text
    #     )
    #     return resp["data"][0]["embedding"]
    # except Exception as e:
    #     raise ModelException(f"Error when hitting OpenAI API: {e}", 500) from e
    #
    # Will use the local encoder as could not find OpenAI 768 dimension embedder
    return encode_by_local_model(text)

def create_embedded_text(event):
    text_to_embed = f"{event.name} | {event.location} | {event.type} | at {event.time}"
    return get_embedding(text_to_embed)