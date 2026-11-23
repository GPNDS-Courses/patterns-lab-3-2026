from abc import ABC, abstractmethod

class AbstractStrategy(ABC):
    @abstractmethod
    def write(self,formatted : str) ->None:
        ...
