from abc import ABC, abstractmethod
from .strategy import AbstractStrategy
from utils import Formatter
from logger import Logger

class AbstractLoggerFactory(ABC):
    @abstractmethod
    def create_strategy(self) -> AbstractStrategy:
        ...

    def create_logger(self, formatter: Formatter | None = None) -> Logger:
        return Logger(self.create_strategy(), formatter)