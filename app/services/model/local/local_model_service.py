from ollama import Client

from app.configuration.config import Config
from app.error_handler.exceptions import ModelException
from app.repositories.event_repository import EventRepository
from app.services.model.model_service import ModelService
from app.util.model_util import get_formatted_prompt


class LocalModelService(ModelService):
    """
    Implementation of ModelService that uses a local Ollama-hosted model
    """

    SYSTEM_PROMPT: str = (
        """
        You are EventFinder, a helpful assistant that summarizes events.
        INSTRUCTIONS:
        1. Use the events provided in context.
        2. Present a concise bullet list of up to {number_of_events} events.
        3. Prioritize events by relevance, popularity, and proximity to the current date.
        RESPONSE FORMAT:
        For each event, use exactly this format:
        - <Event Name>: <Event Type> @ <Venue/Location> (<YYYY-MM-DD>)
        EXAMPLES:
        - Taylor Swift: The Eras Tour: Concert @ Madison Square Garden (2024-08-25)
        """
    )

    def __init__(self, event_repository: EventRepository):
        super().__init__(event_repository)
        self.client = Client()

    def query_prompt(self, user_prompt: str) -> str:
        try:
            sys_prompt = get_formatted_prompt(self.number_of_events, self.SYSTEM_PROMPT)
            messages = self.get_rag_data_and_create_context(user_prompt, sys_prompt)
            prompt_block = "".join(f"[{m['role']}] {m['content']}" for m in messages)
            response = self.client.generate(
                model=Config.LOCAL_MODEL_NAME,
                prompt=prompt_block
            )
            return response.response
        except Exception as e:
            raise ModelException(f"Error while communicating with Ollama API: {e}", 500) from e