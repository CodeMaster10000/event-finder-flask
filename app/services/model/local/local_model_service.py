import subprocess

from app.error_handler.exceptions import ModelException
from app.repositories.event_repository import EventRepository
from app.services.model.model_service import ModelService


class LocalModelService(ModelService):
    """
    Implementation of ModelService that uses a local Ollama-hosted model
    """

    def __init__(self, event_repository: EventRepository, model_name: str = "phi3-mini"):
        super().__init__(event_repository)
        self.model_name = model_name

    def query(self, user_prompt: str) -> str:
        try:
            messages = self.get_rag_data_and_create_context(user_prompt)
            prompt_block = "".join(f"[{m['role']}] {m['content']}" for m in messages)
            result = subprocess.run(
                ["ollama", "run", self.model_name, "--prompt", prompt_block],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.SubprocessError as e:
            raise ModelException(f"Subprocess failed: {e}", 500) from e
        except OSError as e:
            raise ModelException(f"OS-level error launching Ollama: {e}", 500) from e
        except ValueError as e:
            raise ModelException(f"Invalid subprocess parameters: {e}", 500) from e
