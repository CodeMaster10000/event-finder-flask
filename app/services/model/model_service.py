from abc import ABC, abstractmethod
from typing import List, Dict
from app.repositories.event_repository import EventRepository
from app.util.embedding_util import get_embedding


class ModelService(ABC):
    """
    Abstract base class for chat-based event querying.
    """
    # System prompt template for all implementations
    SYSTEM_PROMPT: str = (
        """
        You are EventFinder, a friendly assistant. Use the provided events to answer user queries concisely.
        Use information which is appended in the context, as well as your own information.
        """
    )

    def __init__(self, event_repository: EventRepository):
        """Initialize with an EventRepository for vector search."""
        self.event_repository = event_repository

    @abstractmethod
    def query(self, user_prompt: str) -> str:
        """
        Embed the user prompt, retrieve relevant events, construct messages,
        and return the assistant's text response.
        """
        ...

    def build_messages(self, context: str, user_prompt: str) -> List[Dict[str, str]]:
        """
        Assemble the chat messages with system, assistant, and user roles.
        """
        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "assistant", "content": f"Here are some events I found:\n{context}"},
            {"role": "user", "content": user_prompt},
        ]

    def get_rag_data_and_create_context(self, user_prompt):
        emb = get_embedding(user_prompt)
        hits = self.event_repository.search_by_embedding(emb, k=5)
        context = "\n".join(f"* {h['name']} {h['type']} @ {h['location']} ({h['time']})" for h in hits)
        messages = self.build_messages(context, user_prompt)
        return messages