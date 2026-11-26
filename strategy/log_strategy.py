from pathlib import Path

from abstract import AbstractStrategy

class ConsoleStrategy(AbstractStrategy):
    def write(self, formatted: str) -> None:
        print(formatted)


class FileStrategy(AbstractStrategy):
    def __init__(self, log_file: str | Path = "application.log") -> None:
        self._log_file = Path(log_file)

    def _render(self, formatted: str) -> str:
        return formatted

    def write(self, formatted: str) -> None:
        self._log_file.parent.mkdir(parents=True, exist_ok=True)
        with self._log_file.open("a", encoding="utf-8") as stream:
            stream.write(self._render(formatted) + "\n")


class UpperFileStrategy(FileStrategy):
    def _render(self, formatted: str) -> str:
        return formatted.upper()