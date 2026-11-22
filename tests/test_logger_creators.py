from pathlib import Path

from creators import (
    ConsoleStrategyCreator,
    ErrorStrategyCreator,
    FileStrategyCreator,
    OutputStrategyCreator,
    UpperFileStrategyCreator,
)
from logger import (
    ConsoleOutputStrategy,
    ErrorOutputStrategy,
    FileOutputStrategy,
    Logger,
    LogLevel,
    UpperFileOutputStrategy,
)


# Тест проверяет создание консольной стратегии через ее конкретного создателя.
def test_console_creator_creates_console_strategy() -> None:
    creator = ConsoleStrategyCreator()
    strategy = creator.create()

    assert isinstance(strategy, ConsoleOutputStrategy)


# Тест проверяет создание файловой стратегии через ее конкретного создателя.
def test_file_creator_creates_file_strategy(tmp_path: Path) -> None:
    path = tmp_path / "factory.log"
    creator = FileStrategyCreator()
    strategy = creator.create(path)

    assert isinstance(strategy, FileOutputStrategy)


# Тест проверяет создание верхней файловой стратегии через ее конкретного создателя.
def test_upper_file_creator_creates_upper_file_strategy(tmp_path: Path) -> None:
    path = tmp_path / "factory.log"
    creator = UpperFileStrategyCreator()
    strategy = creator.create(path)

    assert isinstance(strategy, UpperFileOutputStrategy)


# Тест проверяет создание ErrorOutputStrategy и вывод через stderr.
def test_error_creator_creates_error_strategy(capsys) -> None:
    creator = ErrorStrategyCreator()
    strategy = creator.create()

    assert isinstance(strategy, ErrorOutputStrategy)

    logger = Logger(creator)
    logger.log(LogLevel.FATAL, "Critical failure")

    captured = capsys.readouterr()
    assert "[FATAL] Critical failure" in captured.err


# Тест проверяет передачу готовой стратегии из создателя в Logger.
def test_logger_uses_creator_to_create_strategy(capsys) -> None:
    logger = Logger(ConsoleStrategyCreator())

    logger.log(LogLevel.INFO, "Created by factory")

    captured = capsys.readouterr()
    assert "[INFO] Created by factory" in captured.out


# Тест проверяет замену создателя и стратегии во время работы Logger.
def test_logger_can_change_creator(tmp_path: Path) -> None:
    path = tmp_path / "changed.log"
    logger = Logger(ConsoleStrategyCreator())

    logger.set_creator(FileStrategyCreator(), path)
    logger.log(LogLevel.WARN, "Written through another creator")

    text = path.read_text(encoding="utf-8")
    assert "[WARN] Written through another creator" in text


# Негативный тест проверяет, что базовый создатель нельзя создать напрямую.
def test_base_creator_cannot_be_created() -> None:
    try:
        OutputStrategyCreator()
    except TypeError:
        pass
    else:
        raise AssertionError("Ожидалось исключение TypeError")
