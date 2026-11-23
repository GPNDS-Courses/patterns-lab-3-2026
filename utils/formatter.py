from datetime import datetime

from enums.Log import LogLevel

class Formatter:
    @classmethod
    def format(cls, level: LogLevel, message: str) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{timestamp} [{level.value}] {message}"