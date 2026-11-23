
from pathlib import Path

from abstract import AbstractStrategy,AbstractLoggerFactory
from strategy.log_strategy import ConsoleStrategy, FileStrategy, UpperFileStrategy


class ConsoleLoggerFactoryCreator(AbstractLoggerFactory):
    def create_strategy(self) -> AbstractStrategy:
        return ConsoleStrategy()


class FileLoggerFactoryCreator(AbstractLoggerFactory):
    def __init__(self, log_file: str | Path = "application.log") -> None:
        self._log_file = Path(log_file)

    def create_strategy(self) -> AbstractStrategy:
        return FileStrategy(self._log_file)


class UpperFileLoggerCreator(FileLoggerFactoryCreator):
    def create_strategy(self) -> AbstractStrategy:
        return UpperFileStrategy(self._log_file)