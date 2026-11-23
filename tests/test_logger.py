from datetime import datetime
from pathlib import Path

import pytest

from enums import LogLevel
from factory import ConsoleLoggerFactoryCreator, FileLoggerFactoryCreator

LOG_LINE_FORMAT = "%Y-%m-%d %H:%M:%S [INFO] hello"


def test_logger_writes_formatted_message_to_file(tmp_path: Path) -> None:
    log_file = tmp_path / "logs" / "app.log"
    logger = FileLoggerFactoryCreator(log_file).create_logger()

    result = logger.log("INFO", "hello")

    datetime.strptime(result, LOG_LINE_FORMAT)
    assert log_file.read_text(encoding="utf-8") == result + "\n"


def test_logger_prints_formatted_message_to_console(
    capsys: pytest.CaptureFixture[str],
) -> None:
    logger = ConsoleLoggerFactoryCreator().create_logger()

    logger.log(LogLevel.INFO, "hello")

    datetime.strptime(capsys.readouterr().out.strip(), LOG_LINE_FORMAT)


def test_logger_rejects_unknown_level(tmp_path: Path) -> None:
    logger = FileLoggerFactoryCreator(tmp_path / "app.log").create_logger()

    with pytest.raises(ValueError):
        logger.log("debug", "hello")
