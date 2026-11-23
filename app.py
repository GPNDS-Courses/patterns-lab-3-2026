from enums import LogLevel
from factory import (
    ConsoleLoggerFactoryCreator,
    FileLoggerFactoryCreator,
    UpperFileLoggerCreator,
)


def main() -> None:
    console = ConsoleLoggerFactoryCreator().create_logger()
    file = FileLoggerFactoryCreator("logs/app.log").create_logger()
    upper = UpperFileLoggerCreator("logs/app.log").create_logger()

    console.log(LogLevel.INFO, "Application started")
    file.log(LogLevel.WARN, "Low disk space")
    upper.log(LogLevel.ERROR, "Example error")


if __name__ == "__main__":
    main()