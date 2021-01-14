from abc import ABC, abstractmethod
from typing import Any


class Mapper(ABC):

    @abstractmethod
    def map(self, data: Any) -> Any:
        pass
