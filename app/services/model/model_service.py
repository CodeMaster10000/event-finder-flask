from abc import ABC, abstractmethod
from typing import List, Dict

from app.configuration.config import Config
from app.repositories.event_repository import EventRepository
from app.util.embedding_util import get_embedding


class ModelService(ABC):
    """
    Abstract base class for chat-based event querying.
    """

    def __init__(self, event_repository: EventRepository):
        """Initialize with an EventRepository for vector search."""
        self.event_repository = event_repository
        self.number_of_events = Config.NUMBER_OF_EVENTS_TO_SEARCH

    @abstractmethod
    def query_prompt(self, user_prompt: str) -> str:
        """
        Embed the user prompt, retrieve relevant events, construct messages,
        and return the assistant's text response.
        """
        ...

    def build_messages(self, context: str, user_prompt: str, sys_prompt) -> List[Dict[str, str]]:
        """
        Assemble the chat messages with system, assistant, and user roles.
        """
        return [
            {"role": "system", "content": sys_prompt},
            {"role": "assistant", "content": f"Here are some events I found:\n{context}"},
            {"role": "user", "content": user_prompt},
        ]

    def get_rag_data_and_create_context(self, user_prompt, sys_prompt):
        emb = get_embedding(user_prompt)
        hits = self.event_repository.search_by_embedding(emb, self.number_of_events)
        context = "\n".join(f"* {h['name']} {h['type']} @ {h['location']} ({h['time']})" for h in hits)
        messages = self.build_messages(context, user_prompt, sys_prompt)
        return messages
