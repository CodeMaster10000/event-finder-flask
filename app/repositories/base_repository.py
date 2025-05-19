
from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    def get_by_id(self, entity_id: int):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def save(self, entity):
        pass

    @abstractmethod
    def delete_by_id(self, entity_id) -> None:
        pass

    @abstractmethod
    def exists_by_id(self, entity_id):
        pass

    @abstractmethod
    def exists_by_name(self, name: str):
        pass