import openai


def get_embedding(text: str) -> list[float]:
    resp = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return resp["data"][0]["embedding"]

def create_embedded_text(new_event):
    text_to_embed = f"{new_event.name} | {new_event.location} | {new_event.type} | at {new_event.time}"
    return get_embedding(text_to_embed)