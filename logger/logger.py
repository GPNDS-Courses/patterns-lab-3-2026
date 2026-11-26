from abstract import AbstractStrategy
from utils  import Formatter
from enums.Log import LogLevel


class Logger:
    def __init__(
            self,
            strategy: AbstractStrategy,
            formatter: Formatter | None = None,
    ) -> None:
        self._strategy = strategy
        self._formatter = formatter or Formatter()

    def log(self, level: LogLevel | str, message: str) -> str:
        normalized = LogLevel(level)
        formatted = self._formatter.format(normalized, message)
        self._strategy.write(formatted)
        return formatted