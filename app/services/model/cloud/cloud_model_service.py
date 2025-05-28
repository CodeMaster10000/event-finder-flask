import openai
from openai import OpenAIError

from app.configuration.config import Config
from app.error_handler.exceptions import ModelException
from app.repositories.event_repository import EventRepository
from app.services.model.model_service import ModelService
from app.util.model_util import get_formatted_prompt

openai.api_key = Config.CLOUD_MODEL_API_KEY

class CloudModelService(ModelService):
    """
    Implementation of ModelService that uses an OpenAI-hosted model on the cloud
    """

    SYSTEM_PROMPT: str = (
        """
        You are EventFinder, a helpful assistant that summarizes events.
        INSTRUCTIONS:
        1. Use BOTH the events provided in context AND current information from searching for events.
        2. Present a concise bullet list of up to {number_of_events} events.
        3. Prioritize events by relevance, popularity, and proximity to the current date.
        RESPONSE FORMAT:
        For each event, use exactly this format:
        - <Event Name>: <Event Type> @ <Venue/Location> (<YYYY-MM-DD>)
        EXAMPLES:
        - Taylor Swift: The Eras Tour: Concert @ Madison Square Garden (2024-08-25)
        - New York Food Festival: Food Festival @ Central Park (2024-07-15)
        - Yankees vs. Red Sox: Baseball @ Yankee Stadium (2024-06-30)
        If no events match the user's query, explain this clearly and suggest alternative options.
        """
    )

    def __init__(self, event_repository: EventRepository):
        super().__init__(event_repository)

    def query_prompt(self, user_prompt: str):
        try:
            sys_prompt = get_formatted_prompt(self.number_of_events, self.SYSTEM_PROMPT)
            messages = self.get_rag_data_and_create_context(user_prompt, sys_prompt)
            resp = openai.ChatCompletion.create(
                model=Config.CLOUD_MODEL_NAME,
                messages=messages,
                temperature=Config.CLOUD_MODEL_TEMPERATURE,
                max_tokens=Config.CLOUD_MODEL_MAX_TOKENS
            )
        except OpenAIError as e:
            raise ModelException(f"OpenAI API error: {e}", 500) from e
        except Exception as e:
            raise ModelException(f"Unknown error when hitting OpenAI API: {e}", 500) from e
        return resp.choices[0].message.content
