import openai
from app.configuration.config import Config
from app.repositories.event_repository import EventRepository
from app.util.embedding_util import get_embedding

openai.api_key = Config.MODEL_API_KEY

SYSTEM_PROMPT = """
You are EventFinder, a friendly assistant. Use the provided events to answer user queries concisely.
You information which is appended in the context, as well as your own information.
"""

class ChatService:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def query(self, user_prompt: str):
        emb = get_embedding(user_prompt)
        hits = self.event_repository.search_by_embedding(emb, k=5)
        context = "\n".join(f"* {h['name']} {h['type']} @ {h['location']} ({h['time']})" for h in hits)
        messages = self.build_messages(context, user_prompt)
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=400
        )
        return resp.choices[0].message.content

    def build_messages(self, context, user_prompt):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "assistant",
                "content": f"Here are some events I found:\n{context}"
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
        return messages

