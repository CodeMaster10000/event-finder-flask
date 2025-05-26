import openai
from openai import OpenAIError

from app.configuration.config import Config
from app.error_handler.exceptions import ModelException
from app.repositories.event_repository import EventRepository
from app.services.model.model_service import ModelService

openai.api_key = Config.CLOUD_MODEL_API_KEY

class CloudModelService(ModelService):
    """
    Implementation of ModelService that uses an OpenAI-hosted model on the cloud
    """

    def __init__(self, event_repository: EventRepository):
        super().__init__(event_repository)

    def query(self, user_prompt: str):
        try:
            messages = self.get_rag_data_and_create_context(user_prompt)
            resp = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=400
            )
        except OpenAIError as e:
            raise ModelException(f"OpenAI API error: {e}", 500) from e
        except Exception as e:
            raise ModelException(f"Unknown error when hitting OpenAI API: {e}", 500) from e
        return resp.choices[0].message.content
