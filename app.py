from creators import (
    ConsoleStrategyCreator,
    ErrorStrategyCreator,
    FileStrategyCreator,
    UpperFileStrategyCreator,
)
from logger import Logger, LogLevel


def main() -> None:
    console_logger = Logger(ConsoleStrategyCreator())
    console_logger.log(LogLevel.INFO, "Application started")

    file_logger = Logger(FileStrategyCreator(), "logs/app.log")
    file_logger.log(LogLevel.WARN, "Low disk space")

    upper_file_logger = Logger(UpperFileStrategyCreator(), "logs/app.log")
    upper_file_logger.log(LogLevel.ERROR, "Example error")

    error_logger = Logger(ErrorStrategyCreator())
    error_logger.log(LogLevel.FATAL, "Critical failure")


if __name__ == "__main__":
    main()
